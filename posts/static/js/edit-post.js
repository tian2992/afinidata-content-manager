((w) => {
    w.onload = () => {
        const POST_FORM_CONTAINER = document.querySelector('.edit-post-form')

        if(POST_FORM_CONTAINER) {
            const TAGS_DATALIST = document.querySelector('#tags-datalist')
            const TAGS_INPUT = document.querySelector('#tags-input')
            const TAGS_CONTENT = document.querySelector('.tags-content')
            const POST_ID = POST_FORM_CONTAINER.dataset.postId
            const DOMAIN = w.location.origin
            const TAGS_PATH = '/posts/tags'
            const CREATE_TAG_PATH = '/posts/tags/create'
            const POST_TAGS_PATH = (id) => `/posts/${id}/get_tags`
            const ADD_POST_TAG_PATH = (id) => `/posts/${id}/set_tag`

            function createOption(value) {
                let option = document.createElement('option')
                option.value = value
                return option
            }

            function createLabel(item) {
                let label = document.createElement('span')
                label.innerText = item.name
                label.dataset.tagId = item.id
                label.classList.add('tag-item')
                return label
            }

            async function process(event, tags, postTags) {

            }

            async function setInputEvent(input, tags, postTags) {
                let process = async event => {
                    if(event.keyCode === 13) {
                        let tag = tags.find(item => item.name === event.target.value)
                        if(!tag) {
                            let result = await createTag(event.target.value)
                            if(result.status === 'created') {
                                let second_result = await setTagToPost(POST_ID, event.target.value)
                                if(second_result.status !== 'error') {
                                    postTags.push(result.data)
                                }
                                input.value = ""
                                tags.push(result.data)
                                await setPostTags(TAGS_CONTENT, postTags)
                                await setTagsForDataList(TAGS_DATALIST, tags, postTags)
                                input.removeEventListener(process)
                                await setInputEvent(input, tags, postTags)
                            }
                        } else {
                            let postTag = postTags.find(item => item.name === event.target.value)
                            if(!postTag) {
                                let result = await setTagToPost(POST_ID, event.target.value)
                                if(result.status !== 'error') {
                                    input.value = ""
                                    postTags.push(result.data)
                                    await setTagsForDataList(TAGS_DATALIST, tags, postTags)
                                    await setPostTags(TAGS_CONTENT, postTags)
                                    input.removeEventListener(process)
                                    await setInputEvent(input, tags, postTags)
                                }
                            } else {
                                console.log('post has tag')
                            }
                        }
                    }
                }
                input.addEventListener('keyup', process)
            }

            async function createTag(name) {
                let body = new FormData()
                body.append('name', name)
                let uri = `${DOMAIN}${CREATE_TAG_PATH}`
                let result = await fetch(uri, {
                    method: 'post',
                    body
                })
                result = await result.json()
                return result
            }

            async function setTagToPost(id, tagName) {
                let body = new FormData()
                let method = 'post'
                body.append('name', tagName)
                let uri = `${DOMAIN}${ADD_POST_TAG_PATH(id)}`
                let request = await fetch(uri, {method, body})
                let response = await request.json()
                return response
            }

            async function getTags(domain, path) {
                let uri = `${domain}${path}`
                let tags = await fetch(uri, {method: 'get'})
                tags = await tags.json()
                return tags
            }

            async function setTagsForDataList(dataList, tagsArray, postTagsArray) {
                dataList.innerHTML = ""
                console.log(tagsArray)
                console.log(postTagsArray)
                tagsArray.map(tag => console.log(postTagsArray.includes(tag)))
                tagsArray.map(tag => !postTagsArray.includes(tag) && dataList.appendChild(createOption(tag.name)))
            }

            async function setPostTags(element, tags) {
                element.innerHTML = ''
                tags.map(tag => element.appendChild(createLabel(tag)))
            }

            async function main() {
                let tags = await getTags(DOMAIN, TAGS_PATH)
                let postTags = await getTags(DOMAIN, POST_TAGS_PATH(POST_ID))
                tags = tags.data
                postTags = postTags.data
                setPostTags(TAGS_CONTENT, postTags)
                await setTagsForDataList(TAGS_DATALIST, tags, postTags)
                await setInputEvent(TAGS_INPUT, tags, postTags)
            }

            main()
        }
    }
})(window)