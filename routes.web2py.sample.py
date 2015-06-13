#
# Parameters
#

path_prefix = ""
#path_prefix = "web2py-dev" # use when not root application

#
# Do not modify
#

routers = dict(
    BASE = dict(
        default_application = "cryptobib",
        path_prefix = path_prefix,
    ),
)

error_message = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Error</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>

      * {
        line-height: 1.2;
        margin: 0;
      }

      html {
        color: #888;
        display: table;
        font-family: sans-serif;
        height: 100%%;
        text-align: center;
        width: 100%%;
      }

      body {
        display: table-cell;
        vertical-align: middle;
        margin: 2em auto;
      }

      h1 {
        color: #555;
        font-size: 2em;
        font-weight: 400;
      }

      p {
        margin: 0 auto;
        width: 280px;
      }

      @media only screen and (max-width: 280px) {

        body, p {
          width: 95%%;
        }

        h1 {
          font-size: 1.5em;
          margin: 0 0 0.3em;
        }

      }

    </style>
  </head>
  <body>
    <h1>Error</h1>
    <h2>%s</h2>
  </body>
</html>
<!-- IE needs 512+ bytes: http://blogs.msdn.com/b/ieinternals/archive/2010/08/19/http-error-pages-in-internet-explorer.aspx -->"""

error_message_ticket = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Internal error</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>

      * {{
        line-height: 1.2;
        margin: 0;
      }}

      html {{
        color: #888;
        display: table;
        font-family: sans-serif;
        height: 100%%;
        text-align: center;
        width: 100%%;
      }}

      body {{
        display: table-cell;
        vertical-align: middle;
        margin: 2em auto;
      }}

      h1 {{
        color: #555;
        font-size: 2em;
        font-weight: 400;
      }}

      p {{
        margin: 0 auto;
        width: 280px;
      }}

      @media only screen and (max-width: 280px) {{

        body, p {{
          width: 95%%;
        }}

        h1 {{
          font-size: 1.5em;
          margin: 0 0 0.3em;
        }}

      }}

    </style>
  </head>
  <body>
    <h1>Internal error</h1>
    <p>Ticket issued: <a href="{path_prefix}/admin/default/ticket/%(ticket)s" target="_blank">%(ticket)s</a></p
  </body>
</html>""".format(
    path_prefix = "/" + path_prefix if path_prefix != "" else ""
)
