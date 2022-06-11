# spampass
Adds DKIM, DATE, Message_Id headers to SMTP envelope
Modified from https://pypi.org/project/dkimpy/ dkimsign command

## Usage
`cat [smtp.txt] | python3 spampass.py [selector] [domain] [file.key] | nc [reciver-smtp] [25|587]`

"SMTP Envelope" Format
```
EHLO 1.2.3.4
HELO 1.2.3.4
MAIL FROM: support@domain.com
RCPT TO: user@domain.com
data
SENDER: "Lorem ipsum" <support@domain.com>
FROM: "Lorem ipsum" <support@domain.com> 
TO: <user@domain.com>
Subject: !Spoofing Test Email!

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec sollicitudin mi, iaculis malesuada odio. Aliquam non dui at nunc ultricies dictum eget non metus. Duis congue magna ac aliquet condimentum. Suspendisse semper elit sit amet dolor rutrum mattis. Etiam hendrerit blandit nisi sit amet pretium. Aliquam quis rutrum tellus, vitae lacinia ante. Curabitur at scelerisque urna. Vivamus ac mattis felis. Suspendisse potenti. Etiam tincidunt nulla id tellus cursus sagittis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Pellentesque sed semper quam, sed ultrices magna. Pellentesque euismod dolor eget mi bibendum, vitae pellentesque erat commodo. Etiam ut elit vel elit ultricies feugiat vel bibendum neque. Fusce non dictum augue. Nunc elementum, massa ac vulputate eleifend, massa massa pulvinar metus, et lobortis sem arcu et justo.
.

```
