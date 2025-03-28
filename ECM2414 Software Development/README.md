# How to run the tests

The out/ directory contains the compiled classes and the JUnit libraries. To run the tests, you need to create a JAR file that includes the compiled classes and the JUnit libraries. You can then run the tests using the JUnitCore class.

```shell
jar cvf Cards.jar -C out .
java -cp Cards.jar org.junit.runner.JUnitCore test.AllTests
```
