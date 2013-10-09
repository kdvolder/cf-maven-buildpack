CloudFoundry Maven Buildpack
============================

A build pack for CloudFoundry that uses Maven.

This is an experimental build pack for CloudFoundry that uses Maven.  This is different from the standard Java build pack which requires you to build your code locally and upload the compiled bits.  With this build pack your source code is uploaded and built in the CloudFoundry staging environment.  After being built, the application staged and will be run by executing a Maven command (like mvn tomcat7:run).


Instructions
------------

Here are the minimal instructions for using this build pack.

  1. Create a Java / Maven project
  2. Build & Test your application locally with Maven
  3. Run ```cf push --buildpack=https://github.com/dmikusa-pivotal/cf-maven-buildpack.git``` from the root of your project folder.  Alternatively, use "--path" to specify the root of your project.
  4. Your application should start and be running on CloudFoundry.


Behind the Scenes
-----------------

At this point your application has been deployed to CloudFoundry.  This section describes what happened and how you can alter that default behavior. 

First, everything in your application's project folder (or whatever you specified with --path) will be uploaded to CloudFoundry.  You can control what is uploaded by adding a ```.cfignore``` file (same syntax as .gitignore) and specifing files and folders that should not get uploaded.  Minimally, I would suggest adding the ```target``` folder to that list since it would be a waste of bandwidth to upload this folder.

After the upload completes, the build pack will download and install Java and Maven.  It has default versions, which you can see [here](https://github.com/dmikusa-pivotal/cf-maven-buildpack/blob/master/defaults/options.json).  You can change the versions by setting different ```JAVA_PACKAGE```, ```JAVA_PACKAGE_HASH```, ```MAVEN_PACKAGE``` and / or ```MAVEN_PACKAGE_HASH``` tags in your project configuration.

At this point, the build pack will execute ```mvn test``` which should compile and test your application in the CloudFoundry staging environment (Note, if you have long tests you may want to run a different command, staging needs to complete in under 900 seconds).  If you want to change the command that is run add the ```MAVEN_BUILD_COMMAND``` tag into your project configuration and specify a different command to execute.

If your Maven command executes successfully, the build pack will wrap up by doing these two steps.

  1. Copy the Maven local repository into the droplet.  This is done to speed up the initial execution of your application when your application is run.
  2. Create a start script that CloudFoundry will call when the droplet is executed.  By default, the start script is simple.  It sets JAVA_HOME, M2_HOME and calls ```mvn tomcat7:run``` to start your application.  You can specify a different command by setting ```MAVEN_RUN_COMMAND``` in your project configuration file.


Configuration
-------------

In the previous section, I mentioned *project specific configuration*.  Each project can create it's own configuration file which will override the default settings provided by the build pack.  This is done by creating a ```config/options.json``` file in your project folder and populating that file.


Maven Notes
-----------

The build pack should work with most pom.xml files, with only minor modifications.  Here are the adjustments that need to be made for the default configuration, which uses ```tomcat7:run``` to start your application.

  1. In the ```<properties>``` block, add a property ```tomcat.version```.  Set this to the current version of Tomcat.
  
  ```xml
  <properties>
      ...
      <tomcat.version>7.0.42</tomcat.version>
      ...
  </properties>
  ```

  2. Under ```<pluginManagement>``` -> ```<plugins>```, add a ```<plugin>``` tag for ```tomcat-7-maven-plugin.  In here we'll specify the dependencies for the plugin and set the version to what was defined in step #1.

  ```xml
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.tomcat.maven</groupId>
                    <artifactId>tomcat7-maven-plugin</artifactId>
                    <version>2.1</version>
                    <dependencies>
                        <dependency>
                          <groupId>org.apache.tomcat.embed</groupId>
                            <artifactId>tomcat-embed-core</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-util</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-coyote</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-api</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-jdbc</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-dbcp</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-servlet-api</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-jsp-api</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-jasper</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-jasper-el</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-el-api</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-catalina</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-tribes</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-catalina-ha</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-annotations-api</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat</groupId>
                            <artifactId>tomcat-juli</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>

                          <dependency>
                            <groupId>org.apache.tomcat.embed</groupId>
                            <artifactId>tomcat-embed-logging-juli</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>
                          <dependency>
                            <groupId>org.apache.tomcat.embed</groupId>
                            <artifactId>tomcat-embed-logging-log4j</artifactId>
                            <version>${tomcat.version}</version>
                          </dependency>
                     </dependencies>
                </plugin>
            </plugins>
        </pluginManagement>
  ```

  3. Under ```<plugins>``` add a ```<plugin>``` for ```tomcat7-maven-plugin```.  This sets the version of the plugin and is required to set the context path to ```/``` and the port to ```${env.VCAP_APP_PORT}```.

  ```xml
   <plugin>
      <groupId>org.apache.tomcat.maven</groupId>
      <artifactId>tomcat7-maven-plugin</artifactId>
      <version>2.1</version>
      <configuration>
          <port>${env.VCAP_APP_PORT}</port>
          <path>/</path>
      </configuration>
   </plugin>
   ```

