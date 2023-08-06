# Introduction

This documentation covers the usage of the Hosty.Page CLI

# Installation

```shell
pip install hostypage
```

The CLI can be installed with `pip`

# Quick start

> Create a new site

```shell
hostypage publish index.html
```

To publish a site on Hosty.Page, simply call `hostypage publish`, specifying a path to a local HTML 
or zip file. Once the Hosty.Page CLI uploads your file, it will deploy your files to a CDN and return
a URL in the format `https://randomstring.hosty.page`. This site will be live for 24 hours, before it 
expires and will be removed.

<aside class="info">
    With a Hosty.Page Pro account, its possible to extend the expiry, or even remove it completely so
    that sites stay up until they are manually deleted.
</aside>

# Authentication
> Sending API key with single request:

```shell
hostypage publish --api_key myapikey [...args]
```

> Storing the API key locally for future re-use:

```shell
hostypage set-api-key myapikey
```

In order to use the premimum features of Hosty.Page, you will need to authenticate. For free users, there is no need 
to authorize requests. To obtain an API key, you'll need to register for an account at 
<a href="https://hosty.page">Hosty.Page</a>.

Once you have created an account, you can view/change it on the <a href="https://hosty.page/dashboard">Dashboard</a>.

Once you have a valid API key, you can either send it with every single request to the API by passing the `--api-key` 
parameter, or store it locally using the `set-api-key` command.

<aside class="notice">
You must replace <code>myapikey</code> with your own API key.
</aside>

# More publishing options

## Custom domains

> Publish to `randomstring.example.com`

```shell
hostypage publish index.html --domain example.com
``` 


<aside class="warning">
    Pro Feature only
</aside>

<aside class="notice">
    In order to publish sites to a custom domain, you must first create a custom domain in the 
    <a href="https://hosty.page/domains">Domain List</a>, and verify your ownership of it
    by adding the provided CNAME record to your DNS provider.
</aside>

If you have a custom domain, you can pass the `--domain` option to the CLI to publish your
site to this domain.

## Subdomains

> Publish to `customsubdomain.hosty.page`

```shell
hostypage publish index.html --subdomain customsubdomain
``` 

<aside class="warning">
    Pro Feature only
</aside>

Similar to custom domains, it's also possible to publish to a specific subdomain using the
Hosty.Page CLI, by simply passing the `--subdomain argument`.

It's also possible to combine the `--subdomain` and `--domain` parameters to specify
exactly where you want your site to be published.

## Expiry

> Change expiry to 1 week (168 hours)

```shell
hostypage publish index.html --expiry 168
```

> Page never expires

```
hostypage publish index.html --no-expiry
```

<aside class="warning">
    Pro Feature only
</aside>

Hosty.Page lets you customize the expiry of your published sites, or to remove the expiry 
completely so that sites remain live until they are manually deleted. If you do not provide
an expiry option, all published sites will expire and be deleted after 24 hours.

You can change the expiry duration by providing an expiry value, in hours, using the
`--expiry` parameter.

To remove the expiry completely, you can pass the `--no-expiry` parameter.

You may not pass both the `--expiry` and `--no-expiry` fields simultaneously

# API parameter reference

Command | Parameter | Pro account required? | Description
------- | --------- | --------------------- | -----
`set-api-key` | api_key | No | Stores the API key to your local config
`publish` | file | No | The file to publish - Must be a HTML or zip file
`publish` | `--api_key` | No | Passes the API key at the time of publishing
`publish` | `--subdomain` | Yes | Specify the subdomain to publish to
`publish` | `--domain` | Yes | Specify the domain to publish to
`publish` | `--expiry` | Yes | The duration, in hours, before the site gets deleted
`publish` | `--no-expiry` | Yes | Site will never expire

