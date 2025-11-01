    2  grep -rl "isProposedApiEnabled" /usr/lib/code-server/lib/vscode/
   20  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   22  sed -i 's/function xh(i,e){return!0}/function xh(i,e){return i.enabledApiProposals?i.enabledApiProposals.includes(e):!1}/' workbench.js
   23  sed -i 's/function xh(i,e){return!0}/function xh(i,e){return i.enabledApiProposals?i.enabledApiProposals.includes(e):!1}/' /usr/lib/code-server/lib/vscode/out/vs/code/browser/workbench/workbench.js
   24  sudo sed -i 's/function xh(i,e){return!0}/function xh(i,e){return i.enabledApiProposals?i.enabledApiProposals.includes(e):!1}/' /usr/lib/code-server/lib/vscode/out/vs/code/browser/workbench/workbench.js
   25  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   26  vi /usr/lib/code-server/lib/vscode/out/vs/code/browser/workbench/workbench.js
   27  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   28  grep -rl "function isProposedApiEnabled" /usr/lib/code-server/lib/vscode/
   29  vi /usr/lib/code-server/lib/vscode/out/server-main.js.map
   30  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   31  vi /usr/lib/code-server/lib/vscode/out/server-main.js
   32  vi /usr/lib/code-server/lib/vscode/out/vs/workbench/api/worker/extensionHostWorkerMain.js
   33  sudo sed -i 's/function ze(e,t){return!0}/function ze(e,t){return e.enabledApiProposals?e.enabledApiProposals.includes(t):!1}/' /usr/lib/code-server/lib/vscode/out/vs/workbench/api/worker/extensionHostWorkerMain.js
   34  sudo sed -i 's/function nb(e,t){return!0}/function nb(e,t){return e.enabledApiProposals?e.enabledApiProposals.includes(t):!1}/' /usr/lib/code-server/lib/vscode/out/server-main.js
   35  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   36  /usr/lib/code-server/lib/vscode/out/vs/workbench/api/worker/extensionHostWorkerMain.jsvi 
   37  vi /usr/lib/code-server/lib/vscode/out/vs/workbench/api/worker/extensionHostWorkerMain.js
   38  grep -rl "CANNOT use API proposal:" /usr/lib/code-server/lib/vscode/
   39  vi /usr/lib/code-server/lib/vscode/out/vs/workbench/api/node/extensionHostProcess.js
   40  sudo sed -i 's/function Qe(e,t){return!0}/function Qe(e,t){return e.enabledApiProposals?e.enabledApiProposals.includes(t):!1}/' /usr/lib/code-server/lib/vscode/out/vs/workbench/api/node/extensionHostProcess.js
   41  history > patchlepatch.md
