package com.civifix.utils;

import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

import java.util.ArrayList;
import java.util.List;

public class TestListener implements ITestListener {
    private static List<TestResultModel> allResults = new ArrayList<>();

    @Override
    public void onTestSuccess(ITestResult result) {
        addResult(result, "Passed");
    }

    @Override
    public void onTestFailure(ITestResult result) {
        addResult(result, "Failed");
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        addResult(result, "Skipped");
    }

    private void addResult(ITestResult result, String status) {
        String testId = "SEL-TC-" + String.format("%03d", allResults.size() + 1);
        String module = result.getTestClass().getRealClass().getSimpleName().replace("Test", "");
        String scenario = result.getMethod().getMethodName();
        
        // Handle DataProvider parameters dynamically to name the scenario
        if (result.getParameters().length > 0) {
            scenario += " [" + result.getParameters()[0].toString() + "]";
        }
        
        String errorMsg = result.getThrowable() != null ? result.getThrowable().getMessage() : "";
        double duration = (result.getEndMillis() - result.getStartMillis()) / 1000.0;

        allResults.add(new TestResultModel(testId, module, scenario, errorMsg, status, "Chrome Headless", duration));
    }

    @Override
    public void onFinish(ITestContext context) {
        // Generate Dual Reports
        ExcelReportGenerator.generatePassedReport(allResults);
        ExcelReportGenerator.generateFailedReport(allResults);
    }
}
