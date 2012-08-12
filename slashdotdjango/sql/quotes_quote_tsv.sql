-- Add fulltext search vectors to the quotes.

-- add the searchvector column
alter table quotes add column quote_tsv tsvector;

-- create a trigger to keep search vectors up to date.
create trigger before insert or update on quotes for each row execute procedure tsvector_update_trigger(quote_tsv, 'pg_catalog.english', quote);

-- create an index for the vectors to speed up searching.
create index on quotes using gin(quote_tsv);

-- update searchvectors on existing data.
update quotes set quote_tsv=to_tsvector(quote);