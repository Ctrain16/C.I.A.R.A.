'use strict';
require('dotenv').config();
const path = require('path');
const { MongoClient } = require('mongodb');
const { MongoDBProvider } = require('commando-provider-mongo');
const Commando = require('discord.js-commando');
const events = require('./events');

const client = new Commando.Client({
  owner: process.env.MY_DISCORD_ID,
  commandPrefix: 'c ',
});

client.registry
  .registerGroups([['music', 'Music']])
  .registerDefaults()
  .registerCommandsIn(path.join(__dirname, 'commands'));

client.setProvider(
  MongoClient.connect(process.env.MONGO_CONNECTION, {
    useUnifiedTopology: true,
  })
    .then((client) => new MongoDBProvider(client, 'ciaraDataBase'))
    .catch((err) => {
      console.error(err);
    })
);

client
  .on('ready', () => events.online(client))
  .on('guildMemberAdd', (member) => events.welcomeMember(member, client))
  .on('message', (msg) => {});

client.login(process.env.CIARA_TOKEN);
