CloudFoundry Maven Buildpack
----------------------------

A build pack for CloudFoundry that uses Maven.

This is an experimental build pack for CloudFoundry that uses Maven.  This is different from the standard Java build pack which requires you to build your code locally and upload the compiled bits.  With this build pack your source code is uploaded and built in the CloudFoundry staging environment.  After being built, the application staged and will be run by executing a Maven command (like mvn tomcat:run).

This is an experiment to what type of development experience this provides.
