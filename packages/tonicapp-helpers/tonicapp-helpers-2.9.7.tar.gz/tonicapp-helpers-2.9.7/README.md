# Helpers

## Requirements
* Python
* Django
* Django Rest Framework
* DRF spectacular ("https://pypi.org/project/drf-spectacular/")


## Installation

```
$ pip install tonicapp-helpers
```

Add the application to your project's `INSTALLED_APPS` in `settings.py`.

```
INSTALLED_APPS = [
    ...
    'helpers',
]
```


## Source

```
https://pypi.org/project/tonicapp-helpers/
```


## Update Library

```
python3 setup.py sdist
```

```
python3 -m twine upload dist/*
Enter your username: ******
Enter your password: ******
```


# Version updates
From v1.0 to v2.0 the support to drf_spectacular library was removed (the file schema_parameters was removed).


## V2.2.0
Support for views with two different routes. (This should be depecrated in the future)
Support for personalized serializers in requests.

## V2.2.1
Bugfix in permissions when user_id or id not exist

## V2.3.1
Change logger.info to logger.debug in middleware locale.

## V2.4.1
Add CUSTOM_WEB_TOKEN to authentication and IsCustomUserPermission to permissions.

## V2.4.2
Bugfix the prefix match

## V2.4.4
Bugfix the authentication

## V2.5.4
Support to duplications in locale and software type middleware

## V2.6.4
Create new permission: IsAuthenticated

## V2.6.5
In authentication create alternative to run tests

## V2.7.5
Improve the documentation.

## V2.7.6
Bugfix in documentation

## V2.8.6
Add personalized query params to documentation

## V2.9.6
Update information about custom_schemas

## V2.9.7
Fix on permissions (IsCustomUserPermission)
