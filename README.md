# DoS_Attack_Illegal_Service

This script was created to perform a DoS attack/ethical hack on a website that was soliciting illegal services
by automating the creation of the available website form, solving the reCaptcha, and then submitting the "request".

The result was the recipient (criminal) who was soliciting illegal services was blasted with a few thousand
emails. Do not use this script maliciously or against any personal website or service. The author takes no 
responsibility for actions taken on users of this repository. This is for educational purposes only. Be safe :)

Additional Notes: There are obviously many ways to automate this script, in this case it was setup recurringly using a cron
job - but more sophisticated systems will block IP address. Selenium has the capability to use proxy services, and this is
well documented on StackOverflow and official documentation. Proxy services can be used (sometimes at a cost),
but in our case the illegal website was weak and easily exploitable. There are also many alternative ways to perform
DDoS and DoS attacks, all of which should be used for systems testing and ethical hacking only.
