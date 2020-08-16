from P2MT_App import create_app

app = create_app()

# Google Debugger
try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=True
  )
except ImportError:
  pass

if __name__ == "__main__":
    app.run(debug=True)
