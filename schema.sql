
CREATE TABLE IF NOT EXISTS rewards (
    id SERIAL PRIMARY KEY,
    block_number INT NOT NULL,
    transaction_hash VARCHAR(66) NOT NULL,
    log_index INT UNIQUE NOT NULL,
    aix_processed DECIMAL(28, 10) NOT NULL,
    aix_distributed DECIMAL(28, 10) NOT NULL,
    eth_bought DECIMAL(28, 18) NOT NULL,
    eth_distributed_eth DECIMAL(28, 18) NOT NULL,
    -- distributor_wallet VARCHAR(42) NOT NULL,
    -- distributor_balance DECIMAL(28,18) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);