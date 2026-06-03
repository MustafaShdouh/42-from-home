/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:17:28 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>

void	ft_lstclear(t_list **lst, void (*del)(void *))
{
	t_list	*temp;

	if (!lst || !del)
		return ;
	while (*lst)
	{
		temp = (*lst)->next;
		ft_lstdelone(*lst, del);
		*lst = temp;
	}
	*lst = NULL;
}

/*void	del(void *content)
{
    (void)content;
}

int	main(void)
{
	t_list	*head = NULL;
	int		v1 = 1, v2 = 2, v3 = 3;

	ft_lstadd_back(&head, ft_lstnew(&v1));
	ft_lstadd_back(&head, ft_lstnew(&v2));
	ft_lstadd_back(&head, ft_lstnew(&v3));
	printf("List built. Clearing now...\n");
	ft_lstclear(&head, del);
	if (head == NULL)
		printf("Success: Head is NULL.\n");
	else
		printf("Fail: Head still points to %p\n", head);
}*/