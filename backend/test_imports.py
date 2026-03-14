
try:
    from app.main import app
    print("Main app imported successfully!")
except Exception as e:
    import traceback
    print("Error importing app.main:")
    traceback.print_exc()

try:
    from app.api import chat, reports
    print("API modules imported successfully!")
except Exception as e:
    import traceback
    print("Error importing API modules:")
    traceback.print_exc()
