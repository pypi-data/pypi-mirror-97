# Gopublic

[Gopublish](https://github.com/mboudet/gopublish) server.

```bash
# On first use you'll need to create a config file to connect to the server, just run:

$ gopublic init
Welcome to Gopublic
Gopublish server host: localhost
Gopublish server port: 80
Testing connection...
Ok! Everything looks good.
Ready to go! Type `gopublic` to get a list of commands you can execute.

```

This will create a gopublic config file in ~/.gopublic.yml

## Examples

```bash

# List all files
$ gopublic file list
[
    {
        "downloads": 1,
        "file_name": "docker-compose-dev.yml",
        "publishing_date": "2021-03-05",
        "size": 1689,
        "status": "available",
        "uri": "b9ed888a-27c0-4b50-a26f-13105e38b957",
        "version": 3
    },
    {
        "downloads": 0,
        "file_name": "docker-compose-dev.yml",
        "publishing_date": "2021-03-05",
        "size": 1689,
        "status": "available",
        "uri": "269bdb2a-1ad8-4f54-8bc3-be80db81d753",
        "version": 2
    },
    {
        "downloads": 1,
        "file_name": "docker-compose-dev.yml",
        "publishing_date": "2021-03-05",
        "size": 1689,
        "status": "available",
        "uri": "028f89a8-c7f4-4c86-854a-a803ccd7a683",
        "version": 1
    }
]

# Search for either a file name or file ID
$ gopublic file search package.json
[
    {
        "downloads": 1,
        "file_name": "package.json",
        "publishing_date": "2021-03-04",
        "size": 1747,
        "status": "available",
        "uri": "748d469f-7051-47f8-bfdf-af38cedb64c0",
        "version": 1
    }
]

# Publish a file
gopublic file publish '/repos/myrepo_copy/docker-compose-dev.yml' root
{
    "file_id": "46edab15-f482-4ec4-85a5-315d1045306c",
    "message": "File registering. It should be ready soon"
}
```

## License

Available under the MIT License
