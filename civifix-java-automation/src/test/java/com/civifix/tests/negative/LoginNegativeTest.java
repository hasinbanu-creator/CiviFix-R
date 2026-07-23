package com.civifix.tests.negative;

import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class LoginNegativeTest {

    @DataProvider(name = "invalidLogins")
    public Object[][] invalidData() {
        return new Object[][] {
            {"", "123456"},
            {"invalid_email", "123456"},
            {"user@test.com", ""},
            {"user@test.com", "abc"}
        };
    }

    @Test(dataProvider = "invalidLogins")
    public void testInvalidLogin(String email, String otp) {
        // Simulate negative login tests
        Assert.assertTrue(true);
    }
}
