drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  link text not null,
  title text not null,
  value text not null
);
drop table if exists users;
create table users (
  id integer primary key autoincrement,
  email text not null,
  password text not null
);
insert into users (email, password) values ("john@doe.com", "3d3d0d8bc049e2bff8c834b3efa44b54");
insert into users (email, password) values ("jane@doe.com", "3d3d0d8bc049e2bff8c834b3efa44b54");
insert into entries (link, title, value) values ("holmium", "Holmium", "holmium.core provides utility classes to simplify writing pageobjects for webpages using selenium.");
insert into entries (link, title, value) values ("selenium", "Selenium", "Selenium automates browsers. That's it. What you do with that power is entirely up to you. Primarily it is for automating web applications for testing purposes, but is certainly not limited to just that. Boring web-based administration tasks can (and should!) also be automated as well.");
insert into entries (link, title, value) values ("pageobject", "Page Objects", "Within your web app's UI there are areas that your tests interact with. A Page Object simply models these as objects within the test code. This reduces the amount of duplicated code and means that if the UI changes, the fix need only be applied in one place");
