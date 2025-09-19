CREATE TABLE customer_calls (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    phone TEXT,
    transcript TEXT,
    sentiment DECIMAL(5,2),
    insight TEXT,
    solved BOOLEAN
);

INSERT INTO customer_calls (phone, transcript, sentiment, insight, solved) VALUES
('+1234567890', 'Customer called about a billing issue. They are very frustrated with the service and want to cancel their subscription immediately.', -0.85, 'High dissatisfaction with billing service, immediate cancellation risk', FALSE),
('+1234567890', 'Follow-up call after billing issue was resolved. Customer is now satisfied and thanked us for the quick resolution.', 0.75, 'Positive resolution experience, customer retention successful', TRUE),
('+1987654321', 'New customer inquiry about pricing plans. Very interested in the premium package and asked detailed questions.', 0.60, 'High purchase intent for premium package, follow up needed', FALSE),
('+1987654321', 'Customer called to upgrade their plan. Smooth process, very happy with the service so far.', 0.80, 'Successful upsell, customer satisfaction high', TRUE),
('+1555123456', 'Technical support call. Customer having trouble with the mobile app login. Issue resolved quickly.', 0.40, 'Technical issue resolved efficiently, moderate satisfaction', TRUE),
('+1555123456', 'Customer called to report a bug in the dashboard. Slightly frustrated but understanding that it will be fixed.', -0.20, 'Minor technical issue, customer understanding but needs monitoring', FALSE),
('+1444987654', 'Complaint about delivery delay. Customer very upset and threatening to switch to competitor.', -0.90, 'Critical delivery issue, high churn risk, immediate action required', FALSE),
('+1444987654', 'Follow-up after delivery issue resolution. Customer received compensation and is now satisfied.', 0.65, 'Issue resolved with compensation, customer retention achieved', TRUE),
('+1333222111', 'General inquiry about account features. Neutral tone, just gathering information.', 0.10, 'Information gathering call, neutral sentiment, potential for engagement', TRUE),
('+1333222111', 'Customer called to provide feedback on new feature. Very positive about the improvements.', 0.85, 'Positive feedback on new features, strong product satisfaction', TRUE),
('+1777888999', 'Billing dispute call. Customer claims they were overcharged and wants a refund.', -0.70, 'Billing dispute requiring investigation and potential refund', FALSE),
('+1777888999', 'Resolution call after billing dispute. Refund processed, customer satisfied with outcome.', 0.50, 'Billing dispute resolved with refund, customer satisfaction restored', TRUE),
('+1666555444', 'Product demo request. Customer very interested and asking about implementation timeline.', 0.70, 'High interest in product demo, strong sales opportunity', FALSE),
('+1666555444', 'Post-demo follow-up. Customer impressed but needs to discuss with team before decision.', 0.45, 'Positive demo feedback, decision pending team discussion', FALSE),
('+1999888777', 'Cancellation request. Customer citing budget constraints but open to discussing alternatives.', -0.30, 'Budget-driven cancellation, opportunity for retention with alternative solutions', FALSE);
