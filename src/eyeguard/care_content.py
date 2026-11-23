"""General screen-care guidance and references shared by the app and PDF guide."""

CARE_SECTIONS = [
    (
        "During screen sessions",
        [
            "Take regular short breaks and briefly look at something farther away to rest from close-up focusing.",
            "Blink naturally and fully from time to time; do not force repeated blinking if it feels uncomfortable.",
            "Keep the display slightly below eye level when practical, and adjust text size, brightness, and contrast for comfortable reading.",
            "Reduce reflections and strong glare by adjusting the screen angle or nearby lighting.",
        ],
    ),
    (
        "Make your surroundings comfortable",
        [
            "Avoid sitting directly in front of a bright window or a strong light reflected in the screen.",
            "If the room air feels dry, consider whether heating, air conditioning, or a fan is blowing toward your face.",
            "If you wear contact lenses and your eyes feel uncomfortable, follow your lens-care instructions and ask an eye-care professional for advice.",
        ],
    ),
    (
        "Use the app as a reflection tool",
        [
            "Compare your own diary entries over time rather than treating one day or one camera test as a diagnosis.",
            "The blink test is affected by lighting, camera position, glasses, and tracking quality. It does not measure eye disease or prove that a symptom was caused by screen use.",
            "Choose a break interval that suits your routine. EyeGuard's timer is configurable and does not send system notifications.",
        ],
    ),
]

URGENT_GUIDANCE = [
    "Arrange an eye-care appointment if discomfort or dry-eye symptoms persist, keep returning, or interfere with daily activities.",
    "Seek urgent medical or eye-care help for sudden vision loss or change, severe eye pain, a significant eye injury, or a painful red eye (especially while wearing contact lenses).",
]

CARE_SOURCES = [
    (
        "American Academy of Ophthalmology: Computers, Digital Devices, and Eye Strain",
        "https://www.aao.org/eye-health/glasses-contacts/computer-usage",
    ),
    (
        "NHS: Dry eyes - self-care and when to get help",
        "https://www.nhs.uk/symptoms/dry-eyes/",
    ),
    (
        "MediaPipe Face Landmarker documentation",
        "https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker",
    ),
    (
        "Real-Time Eye Blink Detection using Facial Landmarks (Soukupova and Cech, 2016)",
        "https://cmp.felk.cvut.cz/ftp/articles/cech/Soukupova-CVWW-2016.pdf",
    ),
]
