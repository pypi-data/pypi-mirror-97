import sys
import traceback
from functools import cached_property
from typing import Optional, Dict, Any, Callable

import click
import typer
from typer.models import CommandFunctionType

from savvihub.api.exceptions import NotFoundAPIException, InvalidTokenAPIException
from savvihub.cli.config_loader import GlobalConfigLoader
from savvihub.cli.exceptions import ExitException
from savvihub.cli.git import GitRepository
from savvihub.common.constants import DEBUG
from savvihub.exceptions import SavviHubException
from savvihub_client import ResponseMyUser, ResponseProjectInfo


class Context(typer.Context):
    global_config = None
    project_config = None
    git_repo = None

    user: Optional[ResponseMyUser] = None
    project: Optional[ResponseProjectInfo] = None

    store = {}

    def __init__(
        self,
        command,
        parent=None,
        info_name=None,
        obj=None,
        auto_envvar_prefix=None,
        default_map=None,
        terminal_width=None,
        max_content_width=None,
        resilient_parsing=False,
        allow_extra_args=None,
        allow_interspersed_args=None,
        ignore_unknown_options=None,
        help_option_names=None,
        token_normalize_func=None,
        color=None,
        show_default=None,
        # custom
        auth_required=False,
        user_required=False,
    ):
        super().__init__(
            command,
            parent,
            info_name,
            obj,
            auto_envvar_prefix,
            default_map,
            terminal_width,
            max_content_width,
            resilient_parsing,
            allow_extra_args,
            allow_interspersed_args,
            ignore_unknown_options,
            help_option_names,
            token_normalize_func,
            color,
            show_default,
        )
        self.load(auth_required=auth_required, user_required=user_required)

    def load(self, auth_required=False, user_required=False):
        self.global_config = self.load_global_config()
        try:
            if auth_required:
                self.authenticated_client.verify_access_token()
            if user_required:
                self.user = self.authenticated_client.get_my_info()
        except (NotFoundAPIException, InvalidTokenAPIException):
            typer.echo('Token expired. You should run `sv login` first.')
            sys.exit(1)

    def git(self):
        self.git_repo = GitRepository()

    @cached_property
    def authenticated_client(self):
        from savvihub.api.savvihub import SavviHubClient
        return SavviHubClient(token=self.token)

    @cached_property
    def token(self):
        if self.global_config.token:
            return self.global_config.token
        raise ExitException('Login required. You should run `sv login` first.')

    @cached_property
    def workspace(self):
        if self.token and self.global_config.workspace:
            return self.authenticated_client.workspace_read(self.global_config.workspace)

        from savvihub.cli.utils import get_default_workspace
        workspace = get_default_workspace(self.authenticated_client)
        self.global_config.workspace = workspace.name
        return workspace

    @staticmethod
    def load_global_config():
        return GlobalConfigLoader()


class ExceptionMixin:
    def main(self, *args, **kwargs):
        try:
            return super().main(*args, **kwargs)
        except SavviHubException as e:
            if DEBUG:
                typer.echo(traceback.format_exc())

            if e.message:
                typer.echo(e.message)
            sys.exit(e.exit_code)
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            if DEBUG:
                typer.echo(traceback.format_exc())

            # TODO: sentry
            typer.echo('An unexpected exception occurred.')
            sys.exit(1)


class Command(ExceptionMixin, click.Command):
    def make_context(self, info_name, args, parent=None, **extra):
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value

        ctx = Context(self, info_name=info_name, parent=parent, **extra)
        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)

        return ctx

    def get_params(self, ctx):
        rv = self.params
        help_option = self.get_help_option(ctx)
        if help_option is not None:
            rv = [help_option] + rv
        return rv

    def parse_args(self, ctx, args):
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            typer.echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

        parser = self.make_parser(ctx)
        opts, args, _ = parser.parse_args(args=args)

        for param in sorted(self.get_params(ctx), key=lambda p: not p.is_eager):
            value, args = param.handle_parse_result(ctx, opts, args)

        if args and not ctx.allow_extra_args and not ctx.resilient_parsing:
            ctx.fail(
                "Got unexpected extra argument{} ({})".format(
                    "s" if len(args) != 1 else "", " ".join(args)
                )
            )

        ctx.args = args
        return args


class Group(ExceptionMixin, click.Group):
    pass


class Typer(typer.Typer):
    def __init__(self, *args, **kwargs):
        super().__init__(cls=Group, *args, **kwargs)

    def command(
        self,
        name: Optional[str] = None,
        *,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        auth_required: bool = False,
        user_required: bool = False,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        if context_settings is None:
            context_settings = {}

        context_settings.update({
            'auth_required': auth_required,
            'user_required': user_required,
        })

        return super().command(
            name,
            cls=Command,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
        )

    def add_typer(self, *args, **kwargs):
        super().add_typer(cls=Group, *args, **kwargs)
