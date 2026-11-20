// Фикстуры для swift/KazakhPunct.swift: тот же набор, что в scripts/test-kk-punct.py.
//
//   swiftc -o /tmp/kk-punct scripts/test-kk-punct.swift swift/KazakhPunct.swift
//   /tmp/kk-punct
//
import Foundation

func timed(_ phrase: String) -> [TimedWord] {
    var out: [TimedWord] = []
    var t = 0.0
    for token in phrase.split(separator: " ").map(String.init) {
        if token == "|" { t += 0.8; continue }
        out.append(TimedWord(text: token, start: t, end: t + 0.4))
        t += 0.5
    }
    return out
}

@main
struct PunctTest {
    static func main() {
        let cases: [(String, String)] = [
            ("сіз ертең келесіз бе", "Сіз ертең келесіз бе?"),
            ("сіз келесіз бе | құрметті", "Сіз келесіз бе? Құрметті."),
            ("мен бардым | келдім", "Мен бардым. Келдім."),
            ("мен келдім | сен келдің", "Мен келдім. Сен келдің."),
            ("мен үйді | көрдім", "Мен үйді көрдім."),
            ("бұл хабар | айтты", "Бұл хабар айтты."),
            ("ол жұмысшы | келді", "Ол жұмысшы келді."),
            ("мен ертең келемін", "Мен ертең келемін."),
        ]
        var bad = 0
        for (phrase, expected) in cases {
            let got = KazakhPunct.punctuate(timed(phrase))
            let ok = got == expected
            if !ok { bad += 1 }
            print((ok ? "✓" : "✗") + " " + phrase)
            print("   ждали: " + expected)
            print("   вышло: " + got)
        }
        print("\n\(cases.count - bad)/\(cases.count) совпало")
        exit(bad == 0 ? 0 : 1)
    }
}
