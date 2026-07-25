async function detectLayout() {
  if (!navigator.keyboard || !navigator.keyboard.getLayoutMap) {
    console.log("API pas dispo (Firefox/Safari ou pas HTTPS)");
    return;
  }

  const layoutMap = await navigator.keyboard.getLayoutMap();

  const keyQ = layoutMap.get('KeyQ');
  const keyA = layoutMap.get('KeyA');
  const keyW = layoutMap.get('KeyW');
  const keyZ = layoutMap.get('KeyZ');
  const keyY = layoutMap.get('KeyY');

  console.log({ keyQ, keyA, keyW, keyZ, keyY });

  let layout = "inconnu";
  if (keyQ === 'a' && keyA === 'q') layout = "AZERTY";
  else if (keyQ === 'q' && keyZ === 'z') layout = "QWERTY";
  else if (keyQ === 'q' && keyZ === 'y') layout = "QWERTZ";

  console.log("Layout détecté :", layout);
  return layout;
}

detectLayout();
