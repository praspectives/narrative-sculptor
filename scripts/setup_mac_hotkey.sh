#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_NAME="Narrative Sculptor"
WORKFLOW_DIR="$HOME/Library/Services/${WORKFLOW_NAME}.workflow"
CONTENTS_DIR="$WORKFLOW_DIR/Contents"

UUID_ACTION=$(uuidgen)
UUID_INPUT=$(uuidgen)
UUID_OUTPUT=$(uuidgen)

echo "=== Narrative Sculptor — Automator Quick Action Setup ==="
echo ""

mkdir -p "$CONTENTS_DIR"

cat > "$CONTENTS_DIR/document.wflow" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AMApplicationBuild</key>
    <string>521.1</string>
    <key>AMApplicationVersion</key>
    <string>2.10</string>
    <key>AMDocumentVersion</key>
    <string>2</string>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>AMAccepts</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Optional</key>
                    <true/>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>AMActionVersion</key>
                <string>2.0.3</string>
                <key>AMApplication</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>AMParameterProperties</key>
                <dict>
                    <key>COMMAND_STRING</key><dict/>
                    <key>CheckedForUserDefaultShell</key><dict/>
                    <key>inputMethod</key><dict/>
                    <key>shell</key><dict/>
                    <key>source</key><dict/>
                </dict>
                <key>AMProvides</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run Shell Script.action</string>
                <key>ActionName</key>
                <string>Run Shell Script</string>
                <key>ActionParameters</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <string>PATH=\$PATH:/opt/homebrew/bin:/usr/local/bin; cd ~/narrative-sculptor &amp;&amp; uv run sculpt</string>
                    <key>CheckedForUserDefaultShell</key>
                    <true/>
                    <key>inputMethod</key>
                    <integer>0</integer>
                    <key>shell</key>
                    <string>/bin/bash</string>
                    <key>source</key>
                    <string></string>
                </dict>
                <key>BundleIdentifier</key>
                <string>com.apple.RunShellScript</string>
                <key>CFBundleVersion</key>
                <string>2.0.3</string>
                <key>CanShowSelectedItemsWhenRun</key>
                <false/>
                <key>CanShowWhenRun</key>
                <true/>
                <key>Category</key>
                <array>
                    <string>AMCategoryUtilities</string>
                </array>
                <key>Class Name</key>
                <string>RunShellScriptAction</string>
                <key>InputUUID</key>
                <string>${UUID_INPUT}</string>
                <key>Keywords</key>
                <array>
                    <string>Shell</string>
                    <string>Script</string>
                    <string>Run</string>
                    <string>Unix</string>
                </array>
                <key>OutputUUID</key>
                <string>${UUID_OUTPUT}</string>
                <key>UUID</key>
                <string>${UUID_ACTION}</string>
                <key>UnlockWhenRun</key>
                <false/>
                <key>arguments</key>
                <dict/>
                <key>isViewVisible</key>
                <integer>1</integer>
                <key>location</key>
                <string>309.000000:253.000000</string>
                <key>nickname</key>
                <string>Run Shell Script</string>
                <key>selectedHandlerInputParameter</key>
                <string>input</string>
            </dict>
        </dict>
    </array>
    <key>connectors</key>
    <dict/>
    <key>workflowMetaData</key>
    <dict>
        <key>workflowType</key>
        <integer>1</integer>
    </dict>
</dict>
</plist>
EOF

cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSServices</key>
    <array>
        <dict>
            <key>NSMenuItem</key>
            <dict>
                <key>default</key>
                <string>${WORKFLOW_NAME}</string>
            </dict>
            <key>NSMessage</key>
            <string>runWorkflowAsService</string>
            <key>NSSendTypes</key>
            <array/>
        </dict>
    </array>
</dict>
</plist>
EOF

echo "Quick Action installed: $WORKFLOW_DIR"
echo ""
echo "To bind a keyboard shortcut (e.g. Cmd+Shift+E):"
echo "  System Settings → Keyboard → Keyboard Shortcuts → Services"
echo "  Scroll to 'General' → find '${WORKFLOW_NAME}' → click 'Add Shortcut'"
echo ""
echo "Workflow:"
echo "  1. Copy your raw draft to clipboard (Cmd+C)"
echo "  2. Press your hotkey"
echo "  3. Wait for the 'Narrative Sculptor Ready' notification"
echo "  4. Paste (Cmd+V) at the bottom of your document"
