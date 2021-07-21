### parent pom.xml
```
...
<modelVersion>4.0.0</modelVersion>

<groupId>cn.test</groupId>
<artifactId>payment</artifactId>
<version>${revision}</version>
<modules>

    <module>payment-router</module>
    <module>payment-service</module>
    <module>payment-web</module>
    <module>payment-metadata</module>
</modules>

<name>${project.artifactId}</name>
<packaging>pom</packaging>

<properties>
    <revision>2.1.0-SNAPSHOT</revision>
</properties>
...
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>flatten-maven-plugin</artifactId>
    <version>1.0.0</version>
    <configuration>
        <updatePomFile>true</updatePomFile>
    </configuration>
    <executions>
        <execution>
            <id>flatten</id>
            <phase>process-resources</phase>
            <goals>
                <goal>flatten</goal>
            </goals>
        </execution>
        <execution>
            <id>flatten.clean</id>
            <phase>clean</phase>
            <goals>
                <goal>clean</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```
### child pom.xml
```
<parent>
    <artifactId>payment-service</artifactId>
    <groupId>cn.test.service</groupId>
    <version>${revision}</version>
</parent>
<modelVersion>4.0.0</modelVersion>

<artifactId>payment-web</artifactId>
<packaging>jar</packaging>
<properties>
    <test.payment.metadata>${project.version}</test.payment.metadata>
</properties>
<dependencies>
<dependency>
    <groupId>cn.test.service</groupId>
    <artifactId>payment-metadata</artifactId>
    <version>${test.payment.metadata}</version>
</dependency>
</dependencies>
```
