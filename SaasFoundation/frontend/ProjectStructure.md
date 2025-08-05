// Project Structure:
/*
src/
├── components/
│   ├── ui/
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Input.jsx
│   │   ├── Badge.jsx
│   │   ├── Toggle.jsx
│   │   ├── Modal.jsx
│   │   ├── Spinner.jsx
│   │   └── index.js
│   ├── layout/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   └── Layout.jsx
│   ├── auth/
│   │   ├── LoginForm.jsx
│   │   ├── RegisterForm.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── PublicRoute.jsx
│   ├── dashboard/
│   │   ├── DashboardCard.jsx
│   │   ├── StatusCard.jsx
│   │   ├── UsageCard.jsx
│   │   ├── ActivityCard.jsx
│   │   └── QuickActions.jsx
│   ├── subscription/
│   │   ├── PricingCard.jsx
│   │   ├── PlanComparison.jsx
│   │   ├── BillingToggle.jsx
│   │   ├── UsageMetrics.jsx
│   │   └── InvoiceList.jsx
│   ├── team/
│   │   ├── MemberCard.jsx
│   │   ├── InvitationCard.jsx
│   │   ├── InviteForm.jsx
│   │   └── RoleSelect.jsx
│   └── common/
│       ├── ErrorMessage.jsx
│       ├── SuccessMessage.jsx
│       ├── LoadingState.jsx
│       └── EmptyState.jsx
├── pages/
│   ├── Dashboard.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Pricing.jsx
│   ├── Settings.jsx
│   ├── TeamManagement.jsx
│   ├── SubscriptionManagement.jsx
│   ├── EmailVerification.jsx
│   └── InvitationAccept.jsx
├── hooks/
│   ├── useAuth.js
│   ├── useApi.js
│   ├── useSubscription.js
│   └── useTeam.js
├── contexts/
│   ├── AuthContext.jsx
│   ├── ThemeContext.jsx
│   └── NotificationContext.jsx
├── services/
│   ├── api.js
│   ├── auth.js
│   ├── subscription.js
│   └── team.js
├── utils/
│   ├── formatters.js
│   ├── validators.js
│   ├── constants.js
│   └── helpers.js
├── App.jsx
├── index.js
└── index.css
*/
