DK_USER_INVITE_TEMPLATE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>DataKitchen - Invite</title>
        <style type="text/css">
            body {
                margin: 0;
                padding: 0;
                background: #e5e5e5 !important;
            }
            h1, p {
                margin: 0;
            }

            table.body {
                width: 100%;
                height: 100%;
                background: #E5E5E5 !important;
            }

            table.body > tbody > tr > td {
                padding: 48px;
            }

            table.content {
                margin-left: auto;
                margin-right: auto;
                border-radius: 4px;
                border-collapse: collapse;

                background-color: #ffffff;
                background-image: url('https://dk-support-external.s3.amazonaws.com/support/dk_logo_horizontal.png');
                background-repeat: no-repeat;
                background-size: 80px 16px;
                background-position: 16px 16px;
            }

            table.content .content-header {
                padding: 16px;
                padding-bottom: 0px;
            }

            table.content .content-body {
                padding: 16px;
                padding-top: 0px;
                padding-bottom: 75px;
            }

            table.content .content-header h1 {
                font-family: 'Roboto', 'Helvetica Neue', sans-serif;
                font-size: 20px;
                font-weight: 500;
                line-height: 24px;
                color: rgba(0, 0, 0, .87);
                margin-bottom: 75px;
            }

            table.card {
                border: 1px solid rgba(0, 0, 0, 0.12);
                border-radius: 8px;
            }

            .intro {
                font-family: 'Roboto', 'Helvetica Neue', sans-serif;
                font-size: 20px;
                font-weight: 400;
                line-height: 24px;
                color: rgba(0, 0, 0, .87);

                margin-top: 40px;
                margin-bottom: 30px;
            }

            .purpose {
                font-family: 'Roboto', 'Helvetica Neue', sans-serif;
                font-size: 16px;
                font-weight: 400;
                line-height: 18px;
                color: rgba(0, 0, 0, .87);

                margin-bottom: 20px;
            }

            .message {
                font-family: 'Roboto', 'Helvetica Neue', sans-serif;
                font-size: 14px;
                font-weight: 400;
                line-height: 16px;
                color: rgba(0, 0, 0, .38);

                margin-bottom: 40px;
            }

            table.button-table {
                margin-bottom: 40px;
            }

            td.button-wrapper {
                border-radius: 4px;
                background-color: #06A04A;
            }

            td.button-wrapper .button {
                padding: 10px 10px;

                background: #06A04A;
                border-radius: 4px;
                margin: 0px;
                text-decoration: none;

                display: table;
            }

            a.button span {
                font-family: 'Roboto', 'Helvetica Neue', sans-serif;
                font-size: 14px;
                font-weight: 500;
                line-height: 16px;
                color: #ffffff;

                display: table-cell;
                vertical-align: middle;
                padding-right: 8px;
            }

            a.button img {
                width: 18px;
                display: table-cell;
                vertical-align: middle;
            }
        </style>
    </head>
    <body>
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" class="body">
            <tr>
                <td>
                    <table align="center" cellpadding="0" cellspacing="0" width="800" class="content">
                        <tr align="center">
                            <td class="content-header">
                                <!-- <img src="https://dk-support-external.s3.amazonaws.com/support/dk_logo_horizontal.png" alt="DataKitchen" title="DataKitchen" /> -->
                                <h1>DataKitchen - Invite</h1>
                            </td>
                        </tr>

                        <tr>
                            <td class="content-body">
                                <table align="center" cellpadding="0" cellspacing="0" border="0" width="60%" class="card">
                                    <tr>
                                        <td align="center">
                                            <p class="intro">Hey, {{ given_name }}<p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="center">
                                            <p class="purpose">You received an invite to access DataKitchen</p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="center">
                                            <p class="message">Some message here<p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="center">
                                            <table border="0" cellspacing="0" cellpadding="0" class="button-table">
                                                <tr>
                                                    <td align="center" class="button-wrapper">
                                                        <a href="{{ public_address }}/#/join?request_id={{ request_id }}" target="_blank" class="button">
                                                            <!-- TODO: recommend replacing the icon with a &rarr; -->
                                                            <!-- <span>Join Now &rarr;</span> -->

                                                            <span>Join Now</span>
                                                            <img src="https://dk-support-external.s3.amazonaws.com/support/arrow-forward.png" alt="Arrow Forward">

                                                            <!--
                                                            <table border="0" cellspacing="0" cellpadding="0">
                                                                <tr>
                                                                    <td align="center" class="button-wrapper">
                                                                        <span>Join Now</span>
                                                                    </td>
                                                                    <td align="center" class="button-wrapper">
                                                                        <img src="https://dk-support-external.s3.amazonaws.com/support/arrow-forward.png" alt="Arrow Forward">
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            -->
                                                        </a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
"""
