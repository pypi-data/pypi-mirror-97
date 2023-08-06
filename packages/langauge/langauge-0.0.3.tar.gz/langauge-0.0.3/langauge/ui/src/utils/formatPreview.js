// Copyright (c) 2021 FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

// takes in array of token/predictions and formats results
export default function formatPreview(arrayOfTokens) {
  let previewString = "";
  for (let i = 0; i < arrayOfTokens.length; i++) {
    previewString = previewString.concat(
      `["${arrayOfTokens[i]["token"]}", prediction: "${arrayOfTokens[i]["prediction"]}"] \n`
    );
  }
  return previewString;
}
