Fraud Project - GitHub + CI Ready v5
=====================================

هذه النسخة مبنية فوق حزمة Docker/CI السابقة وتضيف:
- .gitignore
- .gitattributes
- README.md
- INIT_GIT_WINDOWS.ps1
- PUSH_TO_GITHUB.ps1
- CHECK_GITHUB_CI_FILES.ps1

الحساب المرتبط حالياً: omerimam
لا يوجد Repository متاح حالياً عبر الاتصال الحالي، لذلك أنشئ Repository فارغاً على GitHub عند مرحلة الرفع فقط.

CI الموجود في:
.github/workflows/ci.yml

يقوم بـ:
Python 3.12
Java 17
Syntax validation
pytest
Docker Compose config validation
FastAPI Docker build
Streamlit Docker build

لا تحتاج تشغيل Docker محلياً الآن.
