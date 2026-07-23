with open("civifix-web/src/hooks/use-dashboard.ts", "r") as f:
    content = f.read()

if "useWorkerDashboard" not in content:
    content += "\nexport function useWorkerDashboard() {\n  return useQuery({\n    queryKey: [\"worker-dashboard\"],\n    queryFn: () => authService.getWorkerDashboard(),\n  });\n}\n"
    with open("civifix-web/src/hooks/use-dashboard.ts", "w") as f:
        f.write(content)
    print("Added useWorkerDashboard")
else:
    print("Already exists")
