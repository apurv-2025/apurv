## 🎉 **Complete Team Management System**

### 🏢 **Organization-Based Architecture**
- **Auto-Organization Creation**: Each user gets a default organization upon registration
- **Multi-Tenant Support**: All subscriptions, billing, and data tied to organizations
- **Role-Based Access Control**: Owner, Admin, and Member roles with different permissions

### 👥 **Team Management Features**

#### **Team Overview** (`/team`)
- **Member List**: View all team members with roles and join dates
- **Role Management**: Admins/owners can change member roles
- **Member Removal**: Remove team members (except owners)
- **Visual Avatars**: Auto-generated user avatars with initials

#### **Invitation System**
- **Email Invitations**: Send professional invitation emails
- **Role Assignment**: Invite users as Member, Admin, or Owner
- **Invitation Management**: View, resend, or cancel pending invitations
- **Expiration Handling**: Invitations expire after 7 days

#### **Invitation Acceptance** (`/invite?token=...`)
- **Smart User Detection**: Handles existing users vs. new signups
- **Account Creation**: New users can create accounts directly from invitations
- **Seamless Login**: Existing users login and auto-accept
- **Security Validation**: Token-based validation with expiration

### 🔐 **Role-Based Permissions**

| Permission | Member | Admin | Owner |
|------------|--------|-------|-------|
| View team members | ✅ | ✅ | ✅ |
| Invite new members | ❌ | ✅ | ✅ |
| Change member roles | ❌ | ✅* | ✅ |
| Remove members | ❌ | ✅* | ✅ |
| Manage organization | ❌ | ✅ | ✅ |
| Billing & subscription | ❌ | View | ✅ |
| Delete organization | ❌ | ❌ | ✅ |

*Admins cannot manage other admins or owners

### 📧 **Email Integration**
- **Professional Templates**: Beautiful HTML email invitations
- **Organization Branding**: Emails include organization name and inviter details
- **Action Links**: Direct links to accept invitations
- **Expiration Notices**: Clear expiration dates in emails

### 🗄️ **Enhanced Database Schema**

#### **New Tables**
- `organizations` - Organization details and settings
- `organization_members` - User-organization relationships with roles
- `invitations` - Pending team invitations with tokens

#### **Updated Structure**
- Subscriptions now tied to organizations (not individual users)
- Payment methods and invoices at organization level
- Usage metrics tracked per organization

### 🔄 **Migration from User-Based to Organization-Based**

The system smoothly transitions from individual user accounts to organization-based:
1. **Existing Users**: Get auto-created organizations
2. **Billing Migration**: Subscriptions move to organization level
3. **Data Integrity**: All existing data preserved and properly linked

### 📱 **Frontend Components**

#### **TeamManagement.js**
- 4-tab interface: Members, Invitations, Invite, Settings
- Real-time member management
- Invitation tracking and management
- Organization settings (for owners)

#### **InvitationAccept.js**
- Token validation and user detection
- Seamless signup/login flow
- Professional invitation display
- Error handling for expired/invalid invitations

### 🎨 **Enhanced UI Features**
- **Role Badges**: Color-coded role indicators
- **Avatar Generation**: Auto-generated user avatars
- **Responsive Design**: Mobile-optimized team management
- **Loading States**: Proper loading indicators
- **Error Handling**: Comprehensive error messages

### 🔗 **API Endpoints**

```
# Organization Management
GET    /organizations/current
PUT    /organizations/current

# Team Members
GET    /organizations/current/members
PUT    /organizations/current/members/{id}
DELETE /organizations/current/members/{id}

# Invitations
POST   /organizations/current/invite
GET    /organizations/current/invitations
DELETE /organizations/current/invitations/{id}
POST   /organizations/current/invitations/{id}/resend

# Invitation Acceptance
GET    /invitations/{token}
POST   /invitations/{token}/accept
```

### 🚀 **Usage Flow**

1. **Owner invites team member** → Email sent with invitation link
2. **Recipient clicks link** → Taken to invitation acceptance page
3. **New user signs up** → Account created and auto-joins team
4. **Existing user logs in** → Auto-accepts and joins team
5. **Team collaboration** → All members work within shared organization

### 🛡️ **Security Features**
- **Token-based invitations** with expiration
- **Email validation** ensures invitations match recipients
- **Role-based access control** prevents unauthorized actions
- **Duplicate prevention** stops multiple invitations to same email

Your SaaS platform now supports **full team collaboration** with enterprise-level user management! 🎉

Test the new features:
```bash
docker-compose down
docker-compose up --build
```

Navigate to **http://localhost:3000/team** to explore the team management features!

------iV3----
Now let me add the CSS styles for the Settings component:Perfect! I've added a comprehensive Settings feature to your SaaS platform. Here's what's now included:

## 🎛️ **Comprehensive Settings Feature**

### **📱 Frontend Settings Component**
- **6 Main Sections**: Profile, Security, Preferences, Notifications, Privacy, Account
- **Tabbed Interface**: Clean sidebar navigation with icons
- **Form Management**: Complete forms with validation and error handling
- **Responsive Design**: Mobile-optimized layout that adapts to smaller screens

### **🔧 Settings Sections Overview**

#### **👤 Profile Tab**
- **Avatar Display**: User initials with gradient background
- **Profile Editing**: First name, last name, email updates
- **Email Verification**: Resend verification emails for unverified accounts
- **Real-time Updates**: Instant feedback on profile changes

#### **🔒 Security Tab** 
- **Password Management**: Change password with current password verification
- **Two-Factor Authentication**: Toggle 2FA (UI ready for implementation)
- **Active Sessions**: View and manage login sessions
- **Security Monitoring**: Login notifications and alerts

#### **⚙️ Preferences Tab**
- **Appearance Settings**: Light/Dark/Auto theme selection
- **Localization**: Language and timezone preferences
- **User Experience**: Customizable interface settings
- **Auto-save**: Preferences saved automatically

#### **🔔 Notifications Tab**
- **Email Controls**: Security alerts, billing notifications, product updates
- **Marketing Preferences**: Marketing emails and promotional content
- **Granular Control**: Individual toggle switches for each notification type
- **Smart Defaults**: Security alerts enabled by default

#### **🛡️ Privacy Tab**
- **Data Export**: Download complete user data in JSON format
- **Data Usage Reports**: See how data is processed and used
- **Third-party Access**: Manage connected applications (UI ready)
- **Privacy Controls**: Comprehensive data management

#### **⚠️ Account Tab**
- **Account Information**: Account ID, member since date, verification status
- **Danger Zone**: Account deletion with confirmation prompts
- **Data Management**: Export before deletion options
- **Security Warnings**: Clear warnings for destructive actions

### **🔗 Backend API Endpoints**

```
PUT  /user/profile          - Update profile information
PUT  /user/password         - Change password
GET  /user/preferences      - Get user preferences  
PUT  /user/preferences      - Update preferences
POST /auth/resend-verification - Resend email verification
GET  /user/export           - Export user data
DELETE /user/account        - Delete account
```

### **✨ Key Features**

#### **🔐 Security Features**
- **Password Validation**: Strength requirements and confirmation
- **Current Password Verification**: Required for password changes
- **Email Re-verification**: When email address is changed
- **Account Deletion Protection**: Confirmation prompts and warnings

#### **📱 User Experience**
- **Responsive Design**: Works perfectly on mobile and desktop
- **Real-time Feedback**: Success/error messages for all actions
- **Form Validation**: Client-side and server-side validation
- **Loading States**: Visual feedback during API calls

#### **🎨 Modern Interface**
- **Clean Design**: Professional settings interface
- **Icon Navigation**: Clear visual indicators for each section  
- **Toggle Switches**: Modern UI elements for preferences
- **Gradient Avatars**: Beautiful user avatar generation

### **🚀 Navigation Integration**

The Settings feature is now fully integrated:
- **Header Navigation**: Settings link in main navigation
- **Dashboard Quick Actions**: Direct link from dashboard
- **Responsive Menu**: Mobile-friendly navigation

### **📱 Usage Flow**

1. **Access Settings**: Click "Settings" in navigation or dashboard
2. **Navigate Sections**: Use sidebar to switch between settings categories
3. **Update Information**: Make changes in any section
4. **Save Changes**: Automatic saving with visual feedback
5. **Manage Account**: Complete account lifecycle management

Your SaaS platform now has enterprise-level settings management! Users can:

- ✅ **Update their profiles** with real-time validation
- ✅ **Manage security settings** including passwords and 2FA
- ✅ **Customize preferences** for theme, language, and notifications  
- ✅ **Control privacy settings** and export their data
- ✅ **Manage their account** including deletion if needed

Try rebuilding and testing the new Settings feature:

```bash
docker-compose down
docker-compose up --build
```

-----------V2

# SaaS Signup System with Pricing & Subscription Management

A comprehensive SaaS platform built with Python FastAPI backend, React frontend, PostgreSQL database, and Docker containerization. Now includes full pricing plans, subscription management, payment processing simulation, and usage tracking.

## 🚀 Features

### **Core Authentication**
- Secure user registration with email verification
- JWT-based authentication with password validation
- Account activation workflow
- User profile management

### **Pricing & Subscription Management**
- **Multiple Pricing Plans**: Free, Starter, Professional, Enterprise
- **Flexible Billing**: Monthly and yearly billing cycles with discounts
- **Plan Upgrades/Downgrades**: Seamless plan changes with prorated billing
- **Subscription Lifecycle**: Active, cancelled, and renewal management
- **Usage Tracking**: Monitor API calls, storage, projects, and team members
- **Feature Limitations**: Enforce plan limits with usage-based restrictions

### **Payment & Billing**
- **Invoice Management**: Automated invoice generation and payment tracking
- **Payment Methods**: Credit card management (simulated)
- **Billing History**: Complete transaction and payment history
- **Tax Calculation**: Automated tax calculation on invoices
- **Payment Processing**: Simulated payment gateway integration

### **Modern Frontend**
- **Responsive Design**: Mobile-first responsive UI
- **Pricing Page**: Interactive pricing comparison with feature matrix
- **Subscription Dashboard**: Complete subscription management interface
- **Usage Analytics**: Real-time usage tracking and visualization
- **Billing Management**: Invoice viewing and payment processing

### **Enterprise Features**
- **Plan Comparison**: Detailed feature comparison matrix
- **Usage Limits**: Enforce plan-based limitations
- **Subscription Analytics**: Track subscription metrics and usage patterns
- **Payment Processing**: Simulated payment gateway with success/failure handling

## 📊 Pricing Plans

| Feature | Free | Starter ($29/mo) | Professional ($99/mo) | Enterprise ($299/mo) |
|---------|------|------------------|----------------------|---------------------|
| Projects | 1 | 5 | Unlimited | Unlimited |
| API Calls/month | 1,000 | 10,000 | 100,000 | Unlimited |
| Storage | 1 GB | 10 GB | 100 GB | Unlimited |
| Team Members | - | 3 | 10 | Unlimited |
| Support | Email | Priority Email | Phone & Email | 24/7 Dedicated |
| Analytics | Basic | Basic | Advanced | Custom |

## 🏗️ Architecture

```
saas-platform/
├── docker-compose.yml          # Container orchestration
├── init.sql                   # Database schema with pricing plans
├── backend/                   # Python FastAPI backend
│   ├── main.py               # API endpoints for subscriptions & billing
│   ├── models.py             # Database models (Users, Plans, Subscriptions, Invoices)
│   ├── schemas.py            # Pydantic schemas for validation
│   ├── auth.py               # JWT authentication
│   └── database.py           # PostgreSQL connection
└── frontend/                  # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── Pricing.js             # Interactive pricing page
    │   │   ├── SubscriptionManagement.js  # Subscription dashboard
    │   │   ├── Dashboard.js           # Updated with subscription info
    │   │   └── ...
    │   ├── contexts/
    │   └── services/
    └── ...
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Gmail account for email functionality (optional)

### 1. Setup Environment

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/saas_app

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### 2. Launch Application

```bash
# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 3. Test the System

1. **Register Account**: Create new user account
2. **Verify Email**: Check email for verification link
3. **Explore Pricing**: Visit `/pricing` to see all plans
4. **Upgrade Subscription**: Test plan upgrades and billing
5. **Manage Subscription**: Use `/subscription` for full management

## 📋 API Endpoints

### **Authentication**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/verify` - Email verification

### **Pricing Plans**
- `GET /pricing/plans` - Get all active pricing plans
- `GET /pricing/plans/{plan_id}` - Get specific plan details

### **Subscription Management**
- `GET /subscriptions/current` - Get current subscription with details
- `POST /subscriptions` - Create/upgrade subscription
- `PUT /subscriptions/{id}` - Update subscription
- `DELETE /subscriptions/{id}` - Cancel subscription

### **Payment & Billing**
- `GET /payment-methods` - Get user's payment methods
- `POST /payment-methods` - Add payment method
- `DELETE /payment-methods/{id}` - Remove payment method
- `GET /invoices` - Get user's invoices
- `POST /invoices/{id}/pay` - Pay invoice (simulated)

### **Usage Tracking**
- `GET /usage` - Get usage metrics
- `POST /usage/{metric_name}` - Record usage

## 🗄️ Database Schema

### **Core Tables**
- `users` - User accounts and profiles
- `pricing_plans` - Available subscription plans
- `subscriptions` - User subscriptions with billing cycles
- `payment_methods` - Stored payment methods
- `invoices` - Billing and payment history
- `usage_metrics` - Usage tracking per user/period
- `verification_tokens` - Email verification tokens

### **Key Features**
- **UUID Primary Keys** for security
- **JSONB Fields** for flexible plan features and limits
- **Proper Indexing** for performance
- **Foreign Key Constraints** for data integrity
- **Timestamp Tracking** for audit trails

## 💳 Payment Processing

The system includes a **simulated payment gateway** that:

- Processes subscription upgrades/downgrades
- Generates invoices with tax calculation
- Handles payment method management
- Tracks payment history and statuses
- Supports both monthly and yearly billing cycles

**Note**: This is a simulation. For production, integrate with Stripe, PayPal, or similar payment processors.

## 📊 Usage Tracking

Monitor and enforce plan limits:

```javascript
// Record API usage
POST /usage/api_calls

// Check current usage
GET /usage?period_start=2024-01-01&period_end=2024-01-31

// Usage metrics include:
// - api_calls
// - storage_gb
// - projects
// - team_members
```

## 🎨 Frontend Components

### **Pricing Page (`/pricing`)**
- Interactive plan comparison
- Monthly/yearly billing toggle
- Feature comparison matrix
- Real-time pricing calculations
- Upgrade/downgrade flows

### **Subscription Management (`/subscription`)**
- **Overview Tab**: Current plan, billing period, features
- **Usage Tab**: Real-time usage metrics with progress bars
- **Billing Tab**: Invoice history and payment processing
- **Payment Methods Tab**: Credit card management

### **Enhanced Dashboard**
- Subscription status overview
- Usage summaries
- Recent billing activity
- Quick action buttons

## 🔧 Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Database Operations

```bash
# Access PostgreSQL
docker exec -it saas-platform_postgres_1 psql -U postgres -d saas_app

# View subscription data
SELECT u.email, p.display_name, s.status, s.billing_cycle 
FROM users u 
JOIN subscriptions s ON u.id = s.user_id 
JOIN pricing_plans p ON s.plan_id = p.id;

# Check usage metrics
SELECT user_id, metric_name, metric_value, period_start 
FROM usage_metrics 
ORDER BY period_start DESC;
```

## 🚀 Production Deployment

### Security Considerations

1. **Environment Variables**:
   - Use strong, unique JWT secrets
   - Secure database credentials
   - Configure proper CORS origins

2. **Payment Integration**:
   - Replace simulated payment with real gateway (Stripe/PayPal)
   - Implement webhooks for payment events
   - Add PCI compliance measures

3. **Database Security**:
   - Enable SSL connections
   - Use connection pooling
   - Regular backups and monitoring

### Performance Optimization

```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - WORKERS=4
    deploy:
      replicas: 3
  
  postgres:
    environment:
      - POSTGRES_SHARED_PRELOAD_LIBRARIES=pg_stat_statements
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 🧪 Testing Scenarios

### **Subscription Flows**
1. Free tier signup → Email verification → Plan upgrade
2. Monthly to yearly billing cycle change
3. Plan downgrade with usage limits
4. Subscription cancellation and reactivation

### **Payment Testing**
1. Invoice generation and payment
2. Payment method addition/removal
3. Failed payment handling
4. Tax calculation verification

### **Usage Tracking**
1. API call tracking and limits
2. Storage usage monitoring
3. Team member management
4. Feature access control

## 📈 Monitoring & Analytics

### **Key Metrics**
- Monthly Recurring Revenue (MRR)
- Customer acquisition and churn rates
- Plan conversion rates
- Usage patterns by plan
- Payment success rates

### **Database Queries**
```sql
-- MRR Calculation
SELECT 
  SUM(CASE WHEN billing_cycle = 'monthly' THEN p.price_monthly 
           WHEN billing_cycle = 'yearly' THEN p.price_yearly / 12 
      END) as mrr
FROM subscriptions s 
JOIN pricing_plans p ON s.plan_id = p.id 
WHERE s.status = 'active';

-- Plan Distribution
SELECT p.display_name, COUNT(*) as subscribers
FROM subscriptions s 
JOIN pricing_plans p ON s.plan_id = p.id 
WHERE s.status = 'active'
GROUP BY p.display_name;
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For questions and support:
- Create GitHub issues for bugs
- Check troubleshooting section
- Review application logs
- Test with provided scenarios

---

**Ready to launch your SaaS platform!** 🚀

The system now includes everything needed for a production-ready SaaS application with comprehensive pricing, subscription management, and billing capabilities.

-----------V1---------

# SaaS Signup System

A comprehensive SaaS signup system built with Python FastAPI backend, React frontend, PostgreSQL database, and Docker containerization.

## Features

- **User Registration & Authentication**
  - Secure user registration with email verification
  - JWT-based authentication
  - Password validation and hashing
  - User profile management

- **Email Verification**
  - Automated email sending with verification links
  - Token-based email verification system
  - Account activation workflow

- **Database Management**
  - PostgreSQL database with proper indexing
  - User management with subscriptions
  - Database migrations and initialization

- **Modern Frontend**
  - React-based responsive UI
  - Protected routes and authentication context
  - Modern design with CSS Grid and Flexbox
  - Real-time form validation

- **Containerized Deployment**
  - Docker containers for all services
  - Docker Compose orchestration
  - Development and production ready

## Project Structure

```
saas-signup-system/
├── docker-compose.yml
├── init.sql
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── database.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── public/
    └── src/
        ├── components/
        ├── contexts/
        ├── services/
        ├── App.js
        ├── App.css
        ├── index.js
        └── index.css
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Gmail account for email functionality (optional)

### 1. Clone and Setup

```bash
# Create project directory
mkdir saas-signup-system
cd saas-signup-system

# Create all the files from the artifacts above
# (Copy each file to its respective location)
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/saas_app

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Email (Optional - for email verification)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### 3. Launch the Application

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## Email Configuration (Optional)

To enable email verification:

1. **Gmail Setup**:
   - Enable 2-factor authentication
   - Generate an app password
   - Use the app password in `EMAIL_PASSWORD`

2. **Environment Variables**:
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-character-app-password
   ```

3. **Other Email Providers**:
   - Update `EMAIL_HOST` and `EMAIL_PORT` accordingly
   - Ensure SMTP credentials are correct

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/verify` - Email verification

### User Management
- `GET /user/profile` - Get user profile
- `GET /user/subscription` - Get subscription details

### Health Check
- `GET /health` - Service health status

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (Unique, Indexed)
- `password_hash`
- `first_name`, `last_name`
- `is_verified`, `is_active`
- `created_at`, `updated_at`

### Verification Tokens Table
- `id` (UUID, Primary Key)
- `user_id` (Foreign Key)
- `token` (Indexed)
- `expires_at`
- `created_at`

### Subscriptions Table
- `id` (UUID, Primary Key)
- `user_id` (Foreign Key, Indexed)
- `plan_name` (Default: 'free')
- `status` (Default: 'active')
- `created_at`, `expires_at`

## Development

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm start
```

### Database Operations

```bash
# Access PostgreSQL container
docker exec -it saas-signup-system_postgres_1 psql -U postgres -d saas_app

# View logs
docker-compose logs postgres
docker-compose logs backend
docker-compose logs frontend
```

## Production Deployment

### Security Considerations

1. **Environment Variables**:
   - Change `JWT_SECRET` to a strong, random key
   - Use secure database credentials
   - Configure proper CORS origins

2. **Database Security**:
   - Use strong PostgreSQL passwords
   - Configure SSL connections
   - Implement connection pooling

3. **Email Security**:
   - Use app-specific passwords
   - Consider using dedicated email services (SendGrid, AWS SES)

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build

# Scale services
docker-compose up --scale backend=3 --scale frontend=2
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Ensure PostgreSQL container is healthy
   - Check database credentials
   - Verify network connectivity

2. **Email Not Sending**:
   - Verify Gmail app password
   - Check SMTP settings
   - Review firewall/network restrictions

3. **CORS Errors**:
   - Ensure frontend URL is in CORS origins
   - Check API_URL configuration

4. **Authentication Issues**:
   - Verify JWT_SECRET consistency
   - Check token expiration
   - Ensure proper header format

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Debug containers
docker exec -it container_name /bin/bash
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Docker and application logs
