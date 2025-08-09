-- Create tables (database is already created by Docker)
CREATE TABLE practitioners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointment_requests (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    practitioner_id INTEGER REFERENCES practitioners(id),
    requested_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'denied')),
    source VARCHAR(20) DEFAULT 'website' CHECK (source IN ('website', 'client_portal', 'ai_agent')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    practitioner_id INTEGER REFERENCES practitioners(id),
    scheduled_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO practitioners (name, specialization, email) VALUES
('Dr. Sarah Johnson', 'General Practice', 'sarah@clinic.com'),
('Dr. Michael Chen', 'Cardiology', 'michael@clinic.com'),
('Dr. Emily Rodriguez', 'Dermatology', 'emily@clinic.com');

INSERT INTO clients (name, email, phone) VALUES
('John Smith', 'john@email.com', '(555) 123-4567'),
('Maria Garcia', 'maria@email.com', '(555) 234-5678'),
('David Wilson', 'david@email.com', '(555) 345-6789');
