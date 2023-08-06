from polidoro_cli.cli import CLI


class Ruby(CLI):
    help = 'Ruby CLI commands'

    def __init__(self):
        super(Ruby, self).__init__(
            commands={
                'console': 'bundle exec rails console',
                'migrate': 'bundle exec rails db:migrate',
                'create': 'bundle exec rails db:create',
                'bundle': 'bundle install',
            },
            aliases={'docker': 'd'},
            helpers={'docker': 'if is to run in the docker container'},
        )

    @classmethod
    def wrapper(cls, name, cmd, **kwargs):
        def wrapper_(*args, docker=False, **_kwargs):
            kwargs.update(_kwargs)
            Ruby.execute(cmd, *args, docker=docker, **kwargs)

        setattr(wrapper_, '__name__', name)
        return wrapper_


Ruby()
