// Chronograph parsers. See PRD §10.
// Priority order: Garmin Xero C1 Pro, LabRadar / LabRadar LX, MagnetoSpeed V3 / Sporter,
// Athlon Rangecraft, ProChrono DLX, Two Box Chrono, Caldwell Chronograph.
// Each parser normalizes to the shared ShotRecord schema (@loadlab/shared).

export type ChronoVendor =
  | "garmin-xero"
  | "labradar"
  | "magnetospeed"
  | "athlon-rangecraft"
  | "prochrono-dlx"
  | "two-box"
  | "caldwell";
