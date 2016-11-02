/**
 * content.jsx: generate main content.
 *
 * Note: this script implements jsx (reactjs) syntax.
 */

import React from 'react';
import DataNew from './import/session-type/data_new.jsx';
import DataAppend from './import/navigation/data_append.jsx';
import ModelGenerate from './import/navigation/model_generate.jsx';
import ModelPredict from './import/navigation/model_predict.jsx';

var AppRouter = React.createClass({
  // display result
    render: function() {
        return(
            <Router>
                <Route path='/' component={this.props.indexRoute} >
                    <IndexRoute component={this.props.indexRoute} />
                    <Route path='/data-new' component={DataNew} />
                    <Route path='/data-append' component={DataAppend} />
                    <Route path='/model-generate' component={ModelGenerate} />
                    <Route path='/model-predict' component={ModelPredict} />
                </Route>
            </Router>
        );
    }
});

// indicate which class can be exported, and instantiated via 'require'
export default AppRouter
