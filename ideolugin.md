<!-- ============================================================================ -->
<!-- Plugin Structure (Maven):                                                  -->
<!-- intellij-gitlab-credential-plugin/                                         -->
<!--   - pom.xml                                                                -->
<!--   - src/main/java/com/example/gitlabcredential/                           -->
<!--       - GitLabCredentialStartupActivity.java                              -->
<!--       - GitLabCredentialConfig.java                                       -->
<!--   - src/main/resources/                                                   -->
<!--       - META-INF/plugin.xml                                               -->
<!-- ============================================================================ -->

<!-- ============================================================================ -->
<!-- File: pom.xml (ROOT OF PROJECT)                                            -->
<!-- ============================================================================ -->
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>gitlab-credential-inserter</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>GitLab Credential Inserter</name>
    <description>Automatically inserts GitLab credentials into IntelliJ's credential store at startup</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <idea.version>2025.2</idea.version>
    </properties>

    <repositories>
        <repository>
            <id>intellij-repository</id>
            <url>https://www.jetbrains.com/intellij-repository/releases</url>
        </repository>
    </repositories>

    <dependencies>
        <!-- IntelliJ Platform SDK -->
        <dependency>
            <groupId>com.jetbrains.intellij.platform</groupId>
            <artifactId>core</artifactId>
            <version>${idea.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.jetbrains.intellij.platform</groupId>
            <artifactId>extensions</artifactId>
            <version>${idea.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Maven Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>

            <!-- Maven Assembly Plugin to create the plugin ZIP -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>3.6.0</version>
                <configuration>
                    <descriptors>
                        <descriptor>src/main/assembly/plugin.xml</descriptor>
                    </descriptors>
                </configuration>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>

<!-- ============================================================================ -->
<!-- File: src/main/assembly/plugin.xml                                          -->
<!-- ============================================================================ -->
<!--
<assembly xmlns="http://maven.apache.org/ASSEMBLY/2.1.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/ASSEMBLY/2.1.0 http://maven.apache.org/xsd/assembly-2.1.0.xsd">
    <id>plugin</id>
    <formats>
        <format>zip</format>
    </formats>
    <includeBaseDirectory>false</includeBaseDirectory>
    <fileSets>
        <fileSet>
            <directory>${project.build.directory}/classes</directory>
            <outputDirectory>gitlab-credential-inserter/lib</outputDirectory>
            <includes>
                <include>**/*</include>
            </includes>
        </fileSet>
    </fileSets>
    <files>
        <file>
            <source>${project.build.directory}/${project.build.finalName}.jar</source>
            <outputDirectory>gitlab-credential-inserter/lib</outputDirectory>
        </file>
    </files>
</assembly>
-->

<!-- ============================================================================ -->
<!-- File: src/main/java/com/example/gitlabcredential/GitLabCredentialStartupActivity.java -->
<!-- ============================================================================ -->
<!--
package com.example.gitlabcredential;

import com.intellij.credentialStore.CredentialAttributes;
import com.intellij.credentialStore.CredentialAttributesKt;
import com.intellij.credentialStore.Credentials;
import com.intellij.ide.passwordSafe.PasswordSafe;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.startup.StartupActivity;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;

/**
 * Startup activity that inserts GitLab credentials into IntelliJ's credential store
 * at IDE startup.
 */
public class GitLabCredentialStartupActivity implements StartupActivity {

    @Override
    public void runActivity(@NotNull Project project) {
        try {
            // Load hardcoded configuration
            GitLabCredentialConfig config = loadConfig();
            
            if (config == null) {
                System.out.println("GitLab credential config is null. Skipping.");
                return;
            }

            // Insert credentials into PasswordSafe (which uses KeePass)
            insertGitLabCredential(config);
            
            System.out.println("✅ GitLab credential inserted successfully!");
            
        } catch (Exception e) {
            System.err.println("❌ Error inserting GitLab credential: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Load configuration - HARDCODED VALUES.
     */
    private GitLabCredentialConfig loadConfig() throws IOException {
        GitLabCredentialConfig config = new GitLabCredentialConfig();
        
        // HARDCODED CONFIGURATION - Replace with your actual values
        config.gitlabServer = "https://gitlab.com";
        config.accountId = "224be9a9-8758-4e0d-bf74-271ebf2f5269";
        config.token = "glpat-your-actual-token-here";  // ⚠️ REPLACE THIS!
        
        return config;
    }

    /**
     * Insert GitLab credential into IntelliJ's credential store.
     */
    private void insertGitLabCredential(GitLabCredentialConfig config) {
        // Create the service name that IntelliJ's GitLab plugin expects
        String serviceName = String.format("GitLab Server %s %s", 
            config.gitlabServer, 
            config.accountId);

        // Create credential attributes
        CredentialAttributes attributes = new CredentialAttributes(
            CredentialAttributesKt.generateServiceName("GitLab", serviceName)
        );

        // Create credentials object with the token
        Credentials credentials = new Credentials(config.accountId, config.token);

        // Store in PasswordSafe (automatically uses KeePass if configured)
        PasswordSafe.getInstance().set(attributes, credentials);

        System.out.println("Stored GitLab credential:");
        System.out.println("  Service: " + serviceName);
        System.out.println("  Account: " + config.accountId);
        System.out.println("  Server: " + config.gitlabServer);
    }
}
-->

<!-- ============================================================================ -->
<!-- File: src/main/java/com/example/gitlabcredential/GitLabCredentialConfig.java -->
<!-- ============================================================================ -->
<!--
package com.example.gitlabcredential;

/**
 * Configuration for GitLab credential.
 */
public class GitLabCredentialConfig {
    public String gitlabServer;
    public String accountId;
    public String token;
}
-->

<!-- ============================================================================ -->
<!-- File: src/main/resources/META-INF/plugin.xml                                -->
<!-- ============================================================================ -->
<!--
<?xml version="1.0" encoding="UTF-8"?>
<idea-plugin>
    <id>com.example.gitlab-credential-inserter</id>
    <name>GitLab Credential Inserter</name>
    <version>1.0.0</version>
    <vendor>Your Name</vendor>
    
    <description><![CDATA[
        Automatically inserts GitLab credentials into IntelliJ's credential store at startup.
        Credentials are hardcoded in the plugin.
    ]]></description>
    
    <depends>com.intellij.modules.platform</depends>
    
    <extensions defaultExtensionNs="com.intellij">
        <postStartupActivity implementation="com.example.gitlabcredential.GitLabCredentialStartupActivity"/>
    </extensions>
</idea-plugin>
-->

<!-- ============================================================================ -->
<!-- BUILD INSTRUCTIONS (MAVEN):                                                 -->
<!-- ============================================================================ -->
<!--

1. Create project structure:
   mkdir -p intellij-gitlab-credential-plugin/src/main/{java/com/example/gitlabcredential,resources/META-INF,assembly}
   cd intellij-gitlab-credential-plugin

2. Create all the files:
   - Copy pom.xml to root
   - Copy plugin.xml to src/main/assembly/
   - Copy GitLabCredentialStartupActivity.java to src/main/java/com/example/gitlabcredential/
   - Copy GitLabCredentialConfig.java to src/main/java/com/example/gitlabcredential/
   - Copy plugin.xml (META-INF) to src/main/resources/META-INF/

   ⚠️ IMPORTANT: Edit GitLabCredentialStartupActivity.java and replace:
      config.token = "glpat-your-actual-token-here"
   with your real GitLab token!

3. Build the plugin:
   mvn clean package

4. The plugin will be created at:
   target/gitlab-credential-inserter-1.0.0-plugin.zip

5. Install the plugin:
   - In IntelliJ: Settings → Plugins → ⚙️ → Install Plugin from Disk
   - Select target/gitlab-credential-inserter-1.0.0-plugin.zip
   - Restart IntelliJ

6. Restart IntelliJ - credentials will be inserted automatically!

TROUBLESHOOTING:
- If Maven can't find IntelliJ dependencies, you may need to use the official plugin:
  Add this plugin to pom.xml instead:
  
  <plugin>
      <groupId>org.jetbrains.intellij.plugins</groupId>
      <artifactId>gradle-intellij-plugin</artifactId>
      <version>1.16.0</version>
  </plugin>

ALTERNATIVE SIMPLE APPROACH:
If Maven dependencies are complex, just manually create the JAR:

1. Compile Java files:
   javac -cp "/path/to/idea/lib/*" src/main/java/com/example/gitlabcredential/*.java -d build/

2. Copy resources:
   cp -r src/main/resources/* build/

3. Create JAR:
   cd build && jar cf gitlab-credential-inserter.jar * && cd ..

4. Create plugin ZIP:
   mkdir -p plugin/lib
   cp build/gitlab-credential-inserter.jar plugin/lib/
   cd plugin && zip -r ../gitlab-credential-inserter-plugin.zip * && cd ..

5. Install the ZIP file in IntelliJ

-->

<!-- ============================================================================ -->
<!-- SIMPLIFIED MANUAL BUILD SCRIPT (NO MAVEN NEEDED):                          -->
<!-- ============================================================================ -->
<!--
#!/bin/bash
# build.sh - Manual build without Maven

set -e

echo "Building IntelliJ GitLab Credential Plugin..."

# Set IDEA_HOME to your IntelliJ installation
IDEA_HOME="/opt/idea"  # Adjust this path!

# Compile
mkdir -p build/classes
javac -cp "$IDEA_HOME/lib/*" \
    -d build/classes \
    src/main/java/com/example/gitlabcredential/*.java

# Copy resources
cp -r src/main/resources/* build/classes/

# Create JAR
cd build/classes
jar cf ../gitlab-credential-inserter.jar *
cd ../..

# Create plugin structure
mkdir -p build/plugin/lib
cp build/gitlab-credential-inserter.jar build/plugin/lib/

# Create ZIP
cd build/plugin
zip -r ../gitlab-credential-inserter-plugin.zip *
cd ../..

echo "✅ Plugin built: build/gitlab-credential-inserter-plugin.zip"
echo "Install it in IntelliJ: Settings → Plugins → Install from Disk"

-->
