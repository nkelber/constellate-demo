# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import constellate

LOGGER = get_logger(__name__)
    

def run():
    st.set_page_config(
        page_title="Constellate Demos"     
    )
    # dataset_id = "7e41317e-740f-e86a-4729-20dab492e925"
    dataset_id = st.sidebar.text_input('Constellate Dataset ID', value='7e41317e-740f-e86a-4729-20dab492e925')
    st.session_state['dataset_id'] = dataset_id
    info = constellate.get_description(dataset_id)
    if 'search_description' in info:
        st.sidebar.write('\u2713 Dataset loaded')

    st.sidebar.success("Select a demo above.")
        

if __name__ == "__main__":
    run()
