from VoiceLock import VoiceLock

lock = VoiceLock()
lock.enroll()
print("Enrollment done. Say 'Woof, cousin' to test.")
if lock.verify():
    print("Verified!")
