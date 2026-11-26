// Representative Kotlin + Jetpack Compose scaffold for MOB-01 (NOT compiled; Android SDK/Gradle NOT installed on host)
package dev.gis.mobile.collector

data class FieldPointUiState(
    val projectId: String = "cairo-field-demo",
    val locationPermissionGranted: Boolean = false,
    val arabicTitle: String = "نقطة معاينة ميدانية",
    val syncQueuePending: Int = 0
)
