-- quotes table
CREATE TABLE quotes (
    created timestamp without time zone DEFAULT now() PRIMARY KEY,
    quote character varying(512) NOT NULL UNIQUE
);

-- Or whatever grants you'd like to give
GRANT ALL ON TABLE quotes TO slashdot;