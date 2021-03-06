/**
 * login.jsx: login link markup.
 *
 * @LoginLink, must be capitalized in order for reactjs to render it as a
 *     component. Otherwise, the variable is rendered as a dom node.
 *
 * Note: this script implements jsx (reactjs) syntax.
 *
 * Note: importing 'named export' (multiple export statements in a module),
 *       requires the object being imported, to be surrounded by { brackets }.
 *
 */

import React from 'react';
import { Link } from 'react-router';
import setLoginState from '../../redux/action/login.jsx';
import setLogoutState from '../../redux/action/logout.jsx';

var LoginLink = React.createClass({
  // call back: return login button
    renderContent: function() {
        if (
            this.props &&
            this.props.user &&
            this.props.user.name == 'anonymous'
        ) {
            return (
                <Link
                    to='/login'
                    activeClassName='active'
                    className='btn mn-2'
                    onClick={this.menuClicked}
                >
                    <span>Sign in</span>
                </Link>
            );
        }
        else {
            return (
                <Link
                    to='/logout'
                    activeClassName='active'
                    className='btn mn-2'
                    onClick={this.menuClicked}
                >
                    <span>Logout</span>
                </Link>
            );
        }
    },
  // logout: remove username from sessionStorage
    menuClicked: function(event) {
        if (
            this.props &&
            this.props.user &&
            !!this.props.user.name &&
            this.props.user.name != 'anonymous'
        ) {
          // update redux store
            var action = setLogoutState();
            this.props.dispatch(action);

          // remove username from sessionStorage
            sessionStorage.removeItem('username');

          // redirect to homepage if logged-out
            browserHistory.push('/');
        }
    },
    render: function(){
        var selectedContent = this.renderContent();
        return(selectedContent);
    }
});

// indicate which class can be exported, and instantiated via 'require'
export default LoginLink
