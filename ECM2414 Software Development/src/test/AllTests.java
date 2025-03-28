package test;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        CardHolderTest.class,
        CardTest.class,
        PackTest.class
})
public class AllTests {
}
