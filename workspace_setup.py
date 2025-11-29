from rpd_core.platform import PlatformServices

ps = PlatformServices()
print("Inbox Folder .................:", ps.fldr_inbox())
print("Outbox Folder ................:", ps.fldr_outbox())
print("Temp Folder ..................:", ps.fldr_temp())
print("Logs Folder ..................:", ps.fldr_logs())
print("Data Folder ..................:", ps.fldr_data())
