import React from 'react';

// Option 1: Simple Image Logo Component
const ImageLogo = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'h-8 w-auto',
    md: 'h-12 w-auto', 
    lg: 'h-16 w-auto',
    xl: 'h-20 w-auto'
  };

  return (
    <div className={`flex justify-center ${className}`}>
      <img 
        src="/logo.png" // Put your logo in public folder
        alt="Company Logo" 
        className={sizeClasses[size]}
      />
    </div>
  );
};

// Option 2: SVG Icon Logo Component  
const SVGLogo = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-12 w-12',
    lg: 'h-16 w-16', 
    xl: 'h-20 w-20'
  };

  return (
    <div className={`flex justify-center ${className}`}>
      <svg 
        className={`${sizeClasses[size]} text-primary-500`} 
        fill="currentColor" 
        viewBox="0 0 24 24"
      >
        {/* Replace this with your actual SVG path */}
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
    </div>
  );
};

// Option 3: Text-based Logo with Gradient
const TextLogo = ({ size = 'md', showTagline = true, className = '' }) => {
  const sizeClasses = {
    sm: 'text-xl',
    md: 'text-3xl',
    lg: 'text-4xl',
    xl: 'text-5xl'
  };

  return (
    <div className={`text-center ${className}`}>
      <h1 className={`${sizeClasses[size]} font-bold text-gradient-primary`}>
        Agentic Practice
      </h1>
      {showTagline && (
        <p className="text-gray-500 text-sm mt-1">
          Simple and Efficient Practice
        </p>
      )}
    </div>
  );
};

// Option 4: Icon + Text Combination Logo
const ComboLogo = ({ size = 'md', layout = 'horizontal', className = '' }) => {
  const iconSizes = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const textSizes = {
    sm: 'text-lg',
    md: 'text-2xl', 
    lg: 'text-3xl',
    xl: 'text-4xl'
  };

  const layoutClasses = layout === 'vertical' 
    ? 'flex-col items-center' 
    : 'items-center';

  const spacingClass = layout === 'vertical' ? 'mb-2' : 'mr-3';

  return (
    <div className={`flex justify-center ${layoutClasses} ${className}`}>
      <div className={`${iconSizes[size]} bg-gradient-primary rounded-lg flex items-center justify-center ${spacingClass}`}>
        <span className="text-white font-bold text-lg">Y</span>
      </div>
      <span className={`${textSizes[size]} font-bold text-gray-900`}>
        YourBrand
      </span>
    </div>
  );
};

// Option 5: Medical/Professional Logo (if it's a healthcare app)
const ProfessionalLogo = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
    xl: 'h-20 w-20'
  };

  return (
    <div className={`flex justify-center ${className}`}>
      <div className={`${sizeClasses[size]} bg-gradient-primary rounded-full flex items-center justify-center shadow-medium`}>
        <svg className="w-1/2 h-1/2 text-white" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
      </div>
    </div>
  );
};

// Export all logo options
export { ImageLogo, SVGLogo, TextLogo, ComboLogo, ProfessionalLogo };

// Main Logo component that you can configure
const Logo = ({ 
  type = 'text', 
  size = 'md', 
  showTagline = true, 
  layout = 'horizontal',
  className = '' 
}) => {
  switch (type) {
    case 'image':
      return <ImageLogo size={size} className={className} />;
    case 'svg':
      return <SVGLogo size={size} className={className} />;
    case 'text':
      return <TextLogo size={size} showTagline={showTagline} className={className} />;
    case 'combo':
      return <ComboLogo size={size} layout={layout} className={className} />;
    case 'professional':
      return <ProfessionalLogo size={size} className={className} />;
    default:
      return <TextLogo size={size} showTagline={showTagline} className={className} />;
  }
};

export default Logo;
