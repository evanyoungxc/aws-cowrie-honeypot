## Additional Panchan Activity

After the original capture, the honeypot continued to see activity consistent with the same Panchan campaign.

On September 25, 2026, another attacker successfully authenticated to the honeypot using:

Username: root
Password: centos
SSH Client: SSH-2.0-Go
HASSH: 98ddc5604ef6a1006a2b49a58759fbe6

The attacker opened an SFTP session, created a randomly named hidden directory, and began uploading another file named `sshd`.

The captured file had the SHA-256:

`c6f5414fe4b8dd00f54004db9c067e896e5e1d67acca7e88746ab6a782785c97`

This was a different hash from the original Panchan sample. However, the new session used the same SSH client fingerprint and followed a very similar SFTP delivery pattern.

Static analysis of the new file also revealed the string:

`pan-chan's mining island hi!`

The binary contained Go packages related to SSH, SFTP, networking, and system information, including:

`golang.org/x/crypto/ssh`

`github.com/pkg/sftp`

These findings provided strong evidence that the new payload was also related to Panchan.

The second capture appeared to be incomplete. Cowrie captured approximately 5.3 MB before the SSH connection closed, while the ELF metadata referenced structures located beyond the end of the captured file. Because of this, I treated the sample as a partial capture rather than attempting to execute or repair it.

This additional activity was useful because I was able to correlate separate attacks using the HASSH fingerprint, delivery method, filename, and static indicators inside the captured payload.
