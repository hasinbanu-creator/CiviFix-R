import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from typing import List
from .load_runner import LoadResult

def generate_load_excel_report(results: List[LoadResult], output_path: str = "CiviFix_LoadTest_Execution_Report.xlsx"):
    wb = openpyxl.Workbook()
    
    # ─── Styles ───────────────────────────────────────────────
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    bold_font = Font(bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))
    
    pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    pass_font = Font(color="006100", bold=True)
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    fail_font = Font(color="9C0006", bold=True)
    
    # Calculate global metrics
    total_reqs = sum(r.total_requests for r in results)
    total_fails = sum(r.failures for r in results)
    total_success = sum(r.successes for r in results)
    global_avg_rt = sum(r.avg_rt * r.total_requests for r in results) / total_reqs if total_reqs else 0
    global_rps = sum(r.rps for r in results)
    
    # ─── 1. Executive Summary ───────────────────────────────
    ws_exec = wb.active
    ws_exec.title = "Executive Summary"
    
    ws_exec.column_dimensions['A'].width = 30
    ws_exec.column_dimensions['B'].width = 20
    
    summary_data = [
        ("CiviFix API Load Test — Executive Summary", ""),
        ("", ""),
        ("Total API Endpoints (Test Cases)", len(results)),
        ("Total Requests Sent", total_reqs),
        ("Total Success", total_success),
        ("Total Failures", total_fails),
        ("Overall Requests Per Second (RPS)", f"{global_rps:.2f}"),
        ("Global Average Response Time", f"{global_avg_rt:.2f} ms"),
        ("Pass Rate", f"{(total_success / total_reqs * 100) if total_reqs else 0:.2f}%")
    ]
    
    for row_idx, (key, val) in enumerate(summary_data, 1):
        cell_k = ws_exec.cell(row=row_idx, column=1, value=key)
        cell_v = ws_exec.cell(row=row_idx, column=2, value=val)
        if row_idx == 1:
            cell_k.font = Font(bold=True, size=16, color="4F81BD")
            ws_exec.merge_cells("A1:B1")
        elif key:
            cell_k.font = bold_font
            cell_k.border = thin_border
            cell_v.border = thin_border
            cell_v.alignment = left_align

    # ─── 2. Module Breakdown ────────────────────────────────
    ws_mod = wb.create_sheet(title="Module Breakdown")
    headers_mod = ["Module", "Endpoints Count", "Total Requests", "RPS", "Avg Response Time (ms)"]
    for col_idx, h in enumerate(headers_mod, 1):
        c = ws_mod.cell(row=1, column=col_idx, value=h)
        c.fill = header_fill
        c.font = header_font
        c.alignment = center_align
        ws_mod.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = 25
        
    modules = {}
    for r in results:
        m = r.scenario.module
        if m not in modules:
            modules[m] = {"endpoints": 0, "reqs": 0, "rps": 0.0, "rt_sum": 0.0}
        modules[m]["endpoints"] += 1
        modules[m]["reqs"] += r.total_requests
        modules[m]["rps"] += r.rps
        modules[m]["rt_sum"] += (r.avg_rt * r.total_requests)
        
    row_idx = 2
    for mod, data in modules.items():
        avg_rt = data["rt_sum"] / data["reqs"] if data["reqs"] else 0
        row_data = [mod, data["endpoints"], data["reqs"], f"{data['rps']:.2f}", f"{avg_rt:.2f}"]
        for col_idx, val in enumerate(row_data, 1):
            c = ws_mod.cell(row=row_idx, column=col_idx, value=val)
            c.border = thin_border
            if col_idx > 1: c.alignment = center_align
        row_idx += 1

    # ─── 3. Detailed Results ────────────────────────────────
    ws_det = wb.create_sheet(title="Detailed Results")
    headers_det = ["Test ID", "Module", "API Endpoint", "Method", "Total Reqs", "RPS", "Min RT (ms)", "Max RT (ms)", "Avg RT (ms)", "Fails", "Status"]
    
    for col_idx, h in enumerate(headers_det, 1):
        c = ws_det.cell(row=1, column=col_idx, value=h)
        c.fill = header_fill
        c.font = header_font
        c.alignment = center_align
        
    ws_det.column_dimensions['A'].width = 10
    ws_det.column_dimensions['B'].width = 20
    ws_det.column_dimensions['C'].width = 45
    ws_det.column_dimensions['D'].width = 10
    ws_det.column_dimensions['E'].width = 12
    ws_det.column_dimensions['F'].width = 10
    ws_det.column_dimensions['G'].width = 12
    ws_det.column_dimensions['H'].width = 12
    ws_det.column_dimensions['I'].width = 12
    ws_det.column_dimensions['J'].width = 10
    ws_det.column_dimensions['K'].width = 12

    for row_idx, r in enumerate(results, 2):
        status = "PASS" if r.failures == 0 else "FAIL"
        
        row_data = [
            r.scenario.tc_id, r.scenario.module, r.scenario.endpoint, r.scenario.method,
            r.total_requests, f"{r.rps:.2f}", f"{r.min_rt:.1f}", f"{r.max_rt:.1f}", f"{r.avg_rt:.1f}",
            r.failures, status
        ]
        
        for col_idx, val in enumerate(row_data, 1):
            c = ws_det.cell(row=row_idx, column=col_idx, value=val)
            c.border = thin_border
            if col_idx >= 5: c.alignment = center_align
            
            if col_idx == 11: # Status column
                if status == "PASS":
                    c.fill = pass_fill
                    c.font = pass_font
                else:
                    c.fill = fail_fill
                    c.font = fail_font

    # ─── 4. Failure & Performance Analysis ──────────────────
    ws_fail = wb.create_sheet(title="Failure Analysis")
    headers_fail = ["Test ID", "API Endpoint", "Reason", "Details"]
    for col_idx, h in enumerate(headers_fail, 1):
        c = ws_fail.cell(row=1, column=col_idx, value=h)
        c.fill = PatternFill(start_color="C0504D", end_color="C0504D", fill_type="solid")
        c.font = header_font
        c.alignment = center_align
    
    ws_fail.column_dimensions['A'].width = 10
    ws_fail.column_dimensions['B'].width = 45
    ws_fail.column_dimensions['C'].width = 30
    ws_fail.column_dimensions['D'].width = 40
    
    row_idx = 2
    for r in results:
        issues = []
        if r.failures > 0:
            issues.append(("API Errors", f"{r.failures} requests failed out of {r.total_requests}"))
        if r.avg_rt > 1000:
            issues.append(("High Latency", f"Average response time {r.avg_rt:.1f}ms exceeds 1000ms threshold"))
            
        for reason, details in issues:
            for col_idx, val in enumerate([r.scenario.tc_id, r.scenario.endpoint, reason, details], 1):
                c = ws_fail.cell(row=row_idx, column=col_idx, value=val)
                c.border = thin_border
                if col_idx == 1: c.alignment = center_align
            row_idx += 1
            
    if row_idx == 2:
        c = ws_fail.cell(row=2, column=1, value="No failures or latency SLA breaches detected.")
        ws_fail.merge_cells("A2:D2")
        c.alignment = center_align
        c.font = Font(italic=True)

    wb.save(output_path)
    print(f"[REPORT] Excel Report generated successfully: {output_path}")
