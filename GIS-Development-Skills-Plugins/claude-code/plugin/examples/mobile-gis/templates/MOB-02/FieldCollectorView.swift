// Representative SwiftUI scaffold for MOB-02 (STRICTLY NOT RUN on Windows; requires macOS + Xcode + CoreLocation)
import Foundation

struct FieldObservationDraft: Codable {
    let featureId: String
    let arabicTitle: String
    let heightDatum: String // "ellipsoidal_wgs84" or "orthometric_egm2008"
}
