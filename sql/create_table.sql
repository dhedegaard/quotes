-- quotes table
CREATE TABLE quotes (
  id serial primary key,
  created timestamp without time zone DEFAULT now(),
  quote text NOT NULL UNIQUE
);

create index quotes_created_idx on quotes(created);

-- Or whatever grants you'd like to give
GRANT ALL ON TABLE quotes TO slashdot;