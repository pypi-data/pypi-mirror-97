import click
from alfa_cli.commands.alfa import alfa


class BaseCliCommand(click.Command):
    def format_usage(self, ctx, formatter):
        """Writes the usage line into the formatter. Adds Global Options."""
        path = ctx.command_path.split(" ")
        path[1:1] = ["[GLOBAL]"]

        pieces = self.collect_usage_pieces(ctx)
        formatter.write_usage(" ".join(path), " ".join(pieces))

    def format_options(self, ctx, formatter):
        """Writes all the options into the formatter if they exist. Also separates Options and Global Options."""

        global_opts = []
        for param in alfa.params:
            if param.name == "version":
                continue

            rv = param.get_help_record(ctx)
            if rv is not None:
                global_opts.append(rv)

        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)

        if global_opts:
            with formatter.section("Global Options"):
                formatter.write_dl(global_opts)
