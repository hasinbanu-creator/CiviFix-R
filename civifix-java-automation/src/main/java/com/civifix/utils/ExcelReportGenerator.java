package com.civifix.utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

public class ExcelReportGenerator {
    private static final String TEMPLATE_PATH = "../Execution_Report.xlsx";

    public static void generatePassedReport(List<TestResultModel> results) {
        generateReport(results.stream().filter(r -> r.getStatus().equalsIgnoreCase("Passed")).collect(Collectors.toList()), "Passed_Execution_Report");
    }

    public static void generateFailedReport(List<TestResultModel> results) {
        generateReport(results.stream().filter(r -> !r.getStatus().equalsIgnoreCase("Passed")).collect(Collectors.toList()), "Failed_Execution_Report");
    }

    private static void generateReport(List<TestResultModel> results, String prefix) {
        if (results.isEmpty() && prefix.contains("Failed")) {
            System.out.println("No failed tests. Skipping failed report generation.");
            return;
        }

        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String outputPath = prefix + "_" + timestamp + ".xlsx";

        try (FileInputStream fis = new FileInputStream(TEMPLATE_PATH);
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = workbook.getSheetAt(0);
            
            int totalTests = results.size();
            long passed = results.stream().filter(r -> r.getStatus().equalsIgnoreCase("Passed")).count();
            long failed = results.stream().filter(r -> r.getStatus().equalsIgnoreCase("Failed")).count();
            long skipped = results.stream().filter(r -> r.getStatus().equalsIgnoreCase("Skipped")).count();
            double passRate = totalTests == 0 ? 0 : (double) passed / totalTests * 100;
            String overallStatus = (failed == 0) ? "PASS" : "FAIL";

            Row totalRow = sheet.getRow(5);
            if(totalRow == null) totalRow = sheet.createRow(5);
            Cell totalCell = totalRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK);
            totalCell.setCellValue(String.valueOf(totalTests));

            Row passedRow = sheet.getRow(6);
            if(passedRow == null) passedRow = sheet.createRow(6);
            passedRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(String.valueOf(passed));

            Row failedRow = sheet.getRow(7);
            if(failedRow == null) failedRow = sheet.createRow(7);
            failedRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(String.valueOf(failed));

            Row skippedRow = sheet.getRow(8);
            if(skippedRow == null) skippedRow = sheet.createRow(8);
            skippedRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(String.valueOf(skipped));

            Row rateRow = sheet.getRow(9);
            if(rateRow == null) rateRow = sheet.createRow(9);
            rateRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(String.format("%.1f%%", passRate));

            Row assessmentRow = sheet.getRow(10);
            if(assessmentRow == null) assessmentRow = sheet.createRow(10);
            assessmentRow.getCell(2, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(overallStatus);
            
            Row timeRow = sheet.getRow(2);
            if(timeRow != null) {
                timeRow.getCell(0, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK).setCellValue(
                    "Execution Time: " + new SimpleDateFormat("MM/dd/yyyy, hh:mm:ss a").format(new Date()) + " | Environment: QA-Selenium | Overall Status: " + overallStatus
                );
            }

            int lastRowNum = sheet.getLastRowNum();
            for (int i = 13; i <= lastRowNum; i++) {
                Row row = sheet.getRow(i);
                if (row != null) {
                    sheet.removeRow(row);
                }
            }

            int startRow = 13;
            CellStyle baseStyle = workbook.createCellStyle();
            baseStyle.setBorderBottom(BorderStyle.THIN);
            baseStyle.setBorderTop(BorderStyle.THIN);
            baseStyle.setBorderLeft(BorderStyle.THIN);
            baseStyle.setBorderRight(BorderStyle.THIN);

            for (TestResultModel r : results) {
                Row row = sheet.createRow(startRow++);
                
                Cell c0 = row.createCell(0); c0.setCellValue(r.getTestId()); c0.setCellStyle(baseStyle);
                Cell c1 = row.createCell(1); c1.setCellValue(r.getModule()); c1.setCellStyle(baseStyle);
                Cell c2 = row.createCell(2); c2.setCellValue(r.getScenario()); c2.setCellStyle(baseStyle);
                Cell c3 = row.createCell(3); c3.setCellValue(r.getErrorMsg()); c3.setCellStyle(baseStyle);
                Cell c4 = row.createCell(4); c4.setCellValue(r.getStatus()); c4.setCellStyle(baseStyle);
                Cell c5 = row.createCell(5); c5.setCellValue(r.getBrowser()); c5.setCellStyle(baseStyle);
                Cell c6 = row.createCell(6); c6.setCellValue(r.getDuration()); c6.setCellStyle(baseStyle);
            }

            try (FileOutputStream fos = new FileOutputStream(outputPath)) {
                workbook.write(fos);
                System.out.println("Generated report: " + outputPath);
            }

        } catch (IOException e) {
            System.err.println("Failed to read template or write report: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
