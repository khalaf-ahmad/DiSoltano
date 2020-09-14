import * as actionTypes from '../actions/actionTypes';
import {
  on_action_fail, on_action_start,
  updateObject
} from '../../shared/utility';

const initial_state = {
  created: [],
  waiting: [],
  loading: false,
  error: "",
};

const fetch_orders_details_success = (state, action) => {
  return updateObject(state, {
    created: [...action.created],
    waiting: [...action.waiting],
    loading: false,
    error: ""
  });
};

const switch_detail = (first, second, detail_id) => {
  let index = first.findIndex(dt => dt.detail_id === detail_id);
  if (index > -1) {
    second.unshift(first[index]);
    first.splice(index, 1);
  }
};

const update_detail_state_success = (state, action) => {
  const detail_id = action.detail_id;
  const created_status = action.created;
  let waiting = [...state.waiting];
  let created = [...state.created];
  if (created_status) {
    switch_detail(waiting, created);
  } else {
    switch_detail(created, waiting);
  }
  return updateObject(state, { waiting, created });
};



export const reducer = (state = initial_state, action) => {
  const type = action.type;
  switch (true) {
    case type === actionTypes.FETCH_ORDERS_DETAILS_SUCCESS:
      return fetch_orders_details_success(state, action);
    case type === actionTypes.UPDATE_DETAIL_STATE_SUCCESS:
      return update_detail_state_success(state, action);
    case type === actionTypes.FETCH_ORDERS_DETAILS_START ||
      type === actionTypes.UPDATE_DETAIL_STATE_START:
      return on_action_start(state, action);
    case type === actionTypes.FETCH_ORDERS_DETAILS_FAIL ||
      type === actionTypes.UPDATE_DETAIL_STATE_FAIL:
      return on_action_fail(state, action);
    default: return state;
  }
};