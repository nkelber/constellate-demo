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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Constellate Demos"     
    )
    import constellate
    st.sidebar.success("Select a demo above.")
    dataset_id = st.text_input('Constellate Dataset ID')
    info = constellate.get_description(dataset_id)
    if 'search_description' in info:
        st.write(info['search_description'])
        st.write('1500 documents sample of ', str(info['num_documents']), ' documents.')
        with st.spinner(text='Downloading...'):
            dataset_file = constellate.get_dataset(dataset_id)
        st.markdown('*Load a new dataset by entering a different dataset ID*')
        

if __name__ == "__main__":
    run()
