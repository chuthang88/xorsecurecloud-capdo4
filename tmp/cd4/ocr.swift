import Foundation
import Vision
import AppKit
let files = CommandLine.arguments.dropFirst()
for file in files {
  let u=URL(fileURLWithPath:file)
  let req=VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.usesLanguageCorrection = false
  req.recognitionLanguages = ["vi-VN", "en-US"]
  do {
    try VNImageRequestHandler(url:u).perform([req])
    let txt=(req.results ?? []).compactMap{$0.topCandidates(1).first?.string}.joined(separator:"\n")
    try txt.write(to:u.deletingPathExtension().appendingPathExtension("txt"),atomically:true,encoding:.utf8)
    print(u.lastPathComponent)
  } catch { print("ERROR \(file): \(error)") }
}
