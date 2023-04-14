import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from './utilities/Container';
import EntryCard from './utilities/EntryCard';
import FileUploader from './utilities/FileUploader';

import { formatDates, sortEntries } from '../helpers/entries';
import { getCookies, isLoggedIn } from '../helpers/setAuthToken';

const Journal = () => {
  const [entries, setEntries] = useState([]);
  const [matchingEntries, setMatchingEntries] = useState([]);
  const history = useHistory();

  useEffect(() => {
    getEntries();
  }, []);

  const getEntries = async () => {
    const token = getCookies().token;
    const headers = {
      'x-auth-token': token
    };
    const res = await axios.get('/api/entries', {headers: headers});
    let data = res.data;
    data = formatDates(data)
    data = sortEntries(data);
    setEntries(data);
    setMatchingEntries(data);
  }


  const searchEntries = (searchInput) => {
    if (searchInput.length > 0) {
      const matches = entries.filter((entry) => {
        return entry.body
          .toLowerCase().includes(searchInput.toLowerCase());
      }
      );
      setMatchingEntries(matches);
    } else {
      setMatchingEntries(entries);
    }
  }


  const renderEntries = () => {
    const entryItems = matchingEntries.map((entry, index) =>
      <EntryCard
        key={entry._id}
        entry={entry}
      />
    );
    return entryItems;
  }


  if (!isLoggedIn()) {
    history.push('/login')
    return null;
  } else {
    return (
      <Container>
        <FileUploader />
        <div className="row">
          <div className="eight columns">
            <h4>Your Entries:</h4>
          </div>
          <div className="four columns">
            <a
              className="button button-primary u-full-width"
              href="/entry"
            >
              Make an Entry
            </a>
          </div>
        </div>
        <div className="row">
          <form>
            <input
              type="text"
              className="u-full-width"
              placeholder="Search for a word or a phrase"
              onChange={(e) => searchEntries(e.target.value)}
              required
            />
          </form>
        </div>
        { renderEntries() }
      </Container>
    );
  }
}

export default Journal;
